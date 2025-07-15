import pandas as pd
import re
from datetime import datetime
import logging

class LogParser:
    """
    A comprehensive log parser that extracts structured information from various log formats
    """
    
    def __init__(self):
        # Common log patterns
        self.patterns = {
            # Custom format: domain IP timestamp type value (like the sample)
            'custom_domain': r'(?P<source>\S+)\s+(?P<ip>\S+)\s+(?P<timestamp>\d+)\s+(?P<severity>\w+)\s+(?P<value>\d+)',
            
            # Standard format: timestamp [severity] source: message
            'standard': r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s*\[?(?P<severity>\w+)\]?\s*(?P<source>\w+)?:?\s*(?P<message>.*)',
            
            # Apache/Nginx format
            'apache': r'(?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s+[+-]\d{4})\s+\[(?P<severity>\w+)\]\s+(?P<message>.*)',
            
            # Syslog format
            'syslog': r'(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(?P<source>\w+)\s+(?P<severity>\w+):\s+(?P<message>.*)',
            
            # Java application logs
            'java': r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+(?P<severity>\w+)\s+\[(?P<source>[^\]]+)\]\s+(?P<message>.*)',
            
            # Generic pattern with just severity and message
            'simple': r'\[?(?P<severity>ERROR|WARN|WARNING|INFO|DEBUG|TRACE|FATAL|CRITICAL)\]?\s*(?P<message>.*)',
            
            # Fallback pattern - just capture everything as message
            'fallback': r'(?P<message>.*)'
        }
        
        # Severity level mapping for normalization
        self.severity_mapping = {
            'FATAL': 'FATAL',
            'CRITICAL': 'FATAL',
            'ERROR': 'ERROR',
            'ERR': 'ERROR',
            'WARN': 'WARNING',
            'WARNING': 'WARNING',
            'INFO': 'INFO',
            'INFORMATION': 'INFO',
            'DEBUG': 'DEBUG',
            'TRACE': 'DEBUG',
            'NOTICE': 'INFO',
            'TEST': 'INFO',
            'REST': 'INFO',
            'JSON': 'INFO',
            'RAW': 'INFO'
        }
    
    def parse_logs(self, log_content):
        """
        Parse log content and return a structured DataFrame
        
        Args:
            log_content (str): Raw log content
            
        Returns:
            pd.DataFrame: Parsed log entries with columns for timestamp, severity, source, message
        """
        lines = log_content.strip().split('\n')
        parsed_entries = []
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
                
            parsed_entry = self._parse_single_line(line, line_num)
            if parsed_entry:
                parsed_entries.append(parsed_entry)
        
        if not parsed_entries:
            return pd.DataFrame()
        
        df = pd.DataFrame(parsed_entries)
        
        # Post-process the data
        df = self._post_process_dataframe(df)
        
        return df
    
    def _parse_single_line(self, line, line_num):
        """
        Parse a single log line using various patterns
        
        Args:
            line (str): Single log line
            line_num (int): Line number for reference
            
        Returns:
            dict: Parsed log entry or None if parsing fails
        """
        line = line.strip()
        if not line:
            return None
        
        # Try each pattern in order of specificity
        for pattern_name, pattern in self.patterns.items():
            try:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    entry = match.groupdict()
                    entry['line_number'] = line_num
                    entry['raw_line'] = line
                    entry['pattern_used'] = pattern_name
                    
                    # Handle custom domain format
                    if pattern_name == 'custom_domain':
                        entry['message'] = f"{entry.get('source', 'unknown')} {entry.get('ip', 'unknown')} {entry.get('severity', 'INFO')} {entry.get('value', 'unknown')}"
                    
                    # Fill in missing fields with defaults
                    entry.setdefault('timestamp', None)
                    entry.setdefault('severity', 'INFO')
                    entry.setdefault('source', 'unknown')
                    entry.setdefault('message', line)
                    
                    return entry
            except Exception as e:
                continue
        
        # If no pattern matches, create a basic entry
        return {
            'timestamp': None,
            'severity': 'INFO',
            'source': 'unknown',
            'message': line,
            'line_number': line_num,
            'raw_line': line,
            'pattern_used': 'fallback'
        }
    
    def _post_process_dataframe(self, df):
        """
        Post-process the parsed DataFrame
        
        Args:
            df (pd.DataFrame): Raw parsed DataFrame
            
        Returns:
            pd.DataFrame: Processed DataFrame
        """
        # Normalize severity levels
        df['severity'] = df['severity'].str.upper().map(
            lambda x: self.severity_mapping.get(x, x) if x else 'INFO'
        )
        
        # Parse timestamps
        df['timestamp'] = df['timestamp'].apply(self._parse_timestamp)
        
        # Clean up source field
        df['source'] = df['source'].fillna('unknown').str.strip()
        
        # Clean up message field
        df['message'] = df['message'].str.strip()
        
        # Add derived fields
        df['has_timestamp'] = df['timestamp'].notna()
        df['message_length'] = df['message'].str.len()
        df['word_count'] = df['message'].str.split().str.len()
        
        # Reorder columns
        column_order = ['timestamp', 'severity', 'source', 'message', 'line_number', 
                       'has_timestamp', 'message_length', 'word_count', 'pattern_used', 'raw_line']
        
        # Only include columns that exist
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    def _parse_timestamp(self, timestamp_str):
        """
        Parse timestamp string into datetime object
        
        Args:
            timestamp_str (str): Timestamp string
            
        Returns:
            datetime or None: Parsed datetime object
        """
        if not timestamp_str or pd.isna(timestamp_str):
            return None
        
        # Common timestamp formats
        formats = [
            '%Y-%m-%d %H:%M:%S.%f',  # 2023-01-01 12:00:00.123
            '%Y-%m-%d %H:%M:%S',     # 2023-01-01 12:00:00
            '%Y-%m-%d %H:%M',        # 2023-01-01 12:00
            '%d/%b/%Y:%H:%M:%S %z',  # 01/Jan/2023:12:00:00 +0000
            '%b %d %H:%M:%S',        # Jan 01 12:00:00
            '%Y-%m-%d',              # 2023-01-01
            '%m/%d/%Y %H:%M:%S',     # 01/01/2023 12:00:00
            '%m-%d-%Y %H:%M:%S',     # 01-01-2023 12:00:00
            '%Y%m%d %H:%M:%S',       # 20230101 12:00:00
            '%Y-%m-%d %H:%M:%S,%f',  # Java format: 2023-01-01 12:00:00,123
        ]
        
        timestamp_str = str(timestamp_str).strip()
        
        # Handle Unix timestamp first (like in the sample)
        if timestamp_str.isdigit():
            try:
                return datetime.fromtimestamp(int(timestamp_str))
            except (ValueError, OSError):
                pass
        
        for fmt in formats:
            try:
                # Handle Java milliseconds format
                if ',%f' in fmt and ',' in timestamp_str:
                    timestamp_str = timestamp_str.replace(',', '.')
                
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        # Try pandas parsing as last resort
        try:
            return pd.to_datetime(timestamp_str, errors='coerce')
        except:
            return None
    
    def get_parsing_stats(self, df):
        """
        Get statistics about the parsing process
        
        Args:
            df (pd.DataFrame): Parsed DataFrame
            
        Returns:
            dict: Parsing statistics
        """
        if df.empty:
            return {'total_lines': 0, 'parsed_lines': 0, 'success_rate': 0}
        
        stats = {
            'total_lines': len(df),
            'parsed_lines': len(df[df['pattern_used'] != 'fallback']),
            'success_rate': len(df[df['pattern_used'] != 'fallback']) / len(df) * 100,
            'patterns_used': df['pattern_used'].value_counts().to_dict(),
            'severities_found': df['severity'].value_counts().to_dict(),
            'sources_found': df['source'].nunique(),
            'timestamp_coverage': df['has_timestamp'].sum() / len(df) * 100,
            'average_message_length': df['message_length'].mean(),
        }
        
        return stats
