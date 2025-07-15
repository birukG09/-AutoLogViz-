"""
SQLite Database Management for AutoLogViz Pro
Handles persistent storage of log data, analysis results, and user preferences
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime
import os

class LogDatabase:
    """SQLite database manager for log analysis platform"""
    
    def __init__(self, db_path="logviz.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp DATETIME,
                severity TEXT,
                source TEXT,
                message TEXT,
                raw_line TEXT,
                line_number INTEGER,
                pattern_used TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                log_id INTEGER,
                anomaly_type TEXT,
                confidence_score REAL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (log_id) REFERENCES logs (id)
            )
        ''')
        
        # Create analysis_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                filename TEXT,
                total_logs INTEGER,
                error_count INTEGER,
                anomaly_count INTEGER,
                processing_engine TEXT,
                analysis_results TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create security_events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                event_type TEXT,
                severity TEXT,
                description TEXT,
                indicators TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_logs(self, session_id, logs_df):
        """Save parsed logs to database"""
        conn = sqlite3.connect(self.db_path)
        
        # Add session_id to dataframe
        logs_df_copy = logs_df.copy()
        logs_df_copy['session_id'] = session_id
        
        # Select only the columns that exist in the database
        required_columns = ['session_id', 'timestamp', 'severity', 'source', 'message', 'raw_line', 'line_number', 'pattern_used']
        
        # Add missing columns with default values
        for col in required_columns:
            if col not in logs_df_copy.columns:
                logs_df_copy[col] = None
        
        # Select only the required columns
        logs_df_final = logs_df_copy[required_columns]
        
        # Save to database
        logs_df_final.to_sql('logs', conn, if_exists='append', index=False)
        
        conn.close()
        return True
    
    def save_anomalies(self, session_id, anomaly_indices, anomaly_data):
        """Save detected anomalies to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for idx in anomaly_indices:
            cursor.execute('''
                INSERT INTO anomalies (session_id, log_id, anomaly_type, confidence_score, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, idx, 'statistical', 0.85, f'Anomaly detected in log entry {idx}'))
        
        conn.commit()
        conn.close()
    
    def save_analysis_session(self, session_id, filename, total_logs, error_count, anomaly_count, engine, results):
        """Save analysis session data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO analysis_sessions 
            (session_id, filename, total_logs, error_count, anomaly_count, processing_engine, analysis_results)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, filename, total_logs, error_count, anomaly_count, engine, json.dumps(results)))
        
        conn.commit()
        conn.close()
    
    def save_security_events(self, session_id, events):
        """Save security analysis events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for event in events:
            cursor.execute('''
                INSERT INTO security_events (session_id, event_type, severity, description, indicators)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, event['type'], event['severity'], event['description'], json.dumps(event.get('indicators', []))))
        
        conn.commit()
        conn.close()
    
    def get_logs(self, session_id=None, limit=1000):
        """Retrieve logs from database"""
        conn = sqlite3.connect(self.db_path)
        
        if session_id:
            query = "SELECT * FROM logs WHERE session_id = ? ORDER BY created_at DESC LIMIT ?"
            df = pd.read_sql_query(query, conn, params=(session_id, limit))
        else:
            query = "SELECT * FROM logs ORDER BY created_at DESC LIMIT ?"
            df = pd.read_sql_query(query, conn, params=(limit,))
        
        conn.close()
        return df
    
    def get_analysis_sessions(self, limit=50):
        """Get recent analysis sessions"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT session_id, filename, total_logs, error_count, anomaly_count, 
                   processing_engine, created_at 
            FROM analysis_sessions 
            ORDER BY created_at DESC 
            LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(limit,))
        
        conn.close()
        return df
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total logs
        cursor.execute("SELECT COUNT(*) FROM logs")
        total_logs = cursor.fetchone()[0]
        
        # Total anomalies
        cursor.execute("SELECT COUNT(*) FROM anomalies")
        total_anomalies = cursor.fetchone()[0]
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM analysis_sessions")
        total_sessions = cursor.fetchone()[0]
        
        # Recent activity (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) FROM logs 
            WHERE created_at >= datetime('now', '-1 day')
        """)
        recent_logs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_logs': total_logs,
            'total_anomalies': total_anomalies,
            'total_sessions': total_sessions,
            'recent_logs': recent_logs
        }
    
    def get_security_events(self, session_id=None, limit=100):
        """Get security events"""
        conn = sqlite3.connect(self.db_path)
        
        if session_id:
            query = "SELECT * FROM security_events WHERE session_id = ? ORDER BY created_at DESC LIMIT ?"
            df = pd.read_sql_query(query, conn, params=(session_id, limit))
        else:
            query = "SELECT * FROM security_events ORDER BY created_at DESC LIMIT ?"
            df = pd.read_sql_query(query, conn, params=(limit,))
        
        conn.close()
        return df
    
    def cleanup_old_data(self, days_old=30):
        """Clean up old data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old logs
        cursor.execute("""
            DELETE FROM logs 
            WHERE created_at < datetime('now', '-{} days')
        """.format(days_old))
        
        # Delete old anomalies
        cursor.execute("""
            DELETE FROM anomalies 
            WHERE created_at < datetime('now', '-{} days')
        """.format(days_old))
        
        # Delete old sessions
        cursor.execute("""
            DELETE FROM analysis_sessions 
            WHERE created_at < datetime('now', '-{} days')
        """.format(days_old))
        
        conn.commit()
        conn.close()