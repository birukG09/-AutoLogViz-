import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import re
from datetime import datetime, timedelta

class AnomalyDetector:
    """
    Advanced anomaly detection for log analysis using multiple statistical and ML methods
    """
    
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
    
    def detect_anomalies(self, df):
        """
        Detect anomalies in log data using multiple methods
        
        Args:
            df (pd.DataFrame): Parsed log DataFrame
            
        Returns:
            list: Indices of anomalous log entries
        """
        if df.empty or len(df) < 10:
            return []
        
        anomaly_scores = []
        
        # Method 1: Statistical anomalies (message length, word count)
        statistical_anomalies = self._detect_statistical_anomalies(df)
        anomaly_scores.append(statistical_anomalies)
        
        # Method 2: Text-based anomalies (unusual message content)
        text_anomalies = self._detect_text_anomalies(df)
        anomaly_scores.append(text_anomalies)
        
        # Method 3: Temporal anomalies (if timestamps available)
        if 'timestamp' in df.columns and df['timestamp'].notna().sum() > 10:
            temporal_anomalies = self._detect_temporal_anomalies(df)
            anomaly_scores.append(temporal_anomalies)
        
        # Method 4: Severity-based anomalies
        severity_anomalies = self._detect_severity_anomalies(df)
        anomaly_scores.append(severity_anomalies)
        
        # Method 5: Pattern-based anomalies
        pattern_anomalies = self._detect_pattern_anomalies(df)
        anomaly_scores.append(pattern_anomalies)
        
        # Combine anomaly scores using ensemble approach
        combined_anomalies = self._combine_anomaly_scores(anomaly_scores, df)
        
        return combined_anomalies
    
    def _detect_statistical_anomalies(self, df):
        """
        Detect anomalies based on statistical measures (message length, word count)
        """
        try:
            features = []
            
            # Message length
            if 'message_length' in df.columns:
                features.append(df['message_length'].values)
            
            # Word count
            if 'word_count' in df.columns:
                features.append(df['word_count'].values)
            
            if not features:
                return np.zeros(len(df))
            
            # Stack features
            X = np.column_stack(features)
            
            # Handle edge cases
            if X.shape[1] == 0 or len(X) < 5:
                return np.zeros(len(df))
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Use Isolation Forest
            anomaly_scores = self.isolation_forest.fit_predict(X_scaled)
            
            # Convert to anomaly scores (1 for normal, -1 for anomaly)
            return (anomaly_scores == -1).astype(float)
            
        except Exception as e:
            return np.zeros(len(df))
    
    def _detect_text_anomalies(self, df):
        """
        Detect anomalies based on text content using TF-IDF and clustering
        """
        try:
            messages = df['message'].fillna('').astype(str)
            
            if len(messages) < 5:
                return np.zeros(len(df))
            
            # Clean messages for analysis
            cleaned_messages = [self._clean_message(msg) for msg in messages]
            
            # TF-IDF vectorization
            tfidf_matrix = self.tfidf.fit_transform(cleaned_messages)
            
            if tfidf_matrix.shape[1] == 0:
                return np.zeros(len(df))
            
            # Use DBSCAN clustering to identify outliers
            dbscan = DBSCAN(eps=0.5, min_samples=3, metric='cosine')
            clusters = dbscan.fit_predict(tfidf_matrix.toarray())
            
            # Points labeled as -1 are considered outliers
            text_anomalies = (clusters == -1).astype(float)
            
            return text_anomalies
            
        except Exception as e:
            return np.zeros(len(df))
    
    def _detect_temporal_anomalies(self, df):
        """
        Detect temporal anomalies (bursts, gaps, unusual timing patterns)
        """
        try:
            # Filter rows with valid timestamps
            df_with_time = df[df['timestamp'].notna()].copy()
            
            if len(df_with_time) < 10:
                return np.zeros(len(df))
            
            df_with_time = df_with_time.sort_values('timestamp')
            
            # Calculate time differences between consecutive log entries
            time_diffs = df_with_time['timestamp'].diff().dt.total_seconds()
            time_diffs = time_diffs.dropna()
            
            if len(time_diffs) < 5:
                return np.zeros(len(df))
            
            # Detect anomalous time gaps using statistical thresholds
            q75, q25 = np.percentile(time_diffs, [75, 25])
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            
            # Mark entries with unusual time gaps
            anomalous_time_diffs = (time_diffs < lower_bound) | (time_diffs > upper_bound)
            
            # Create anomaly array for original DataFrame
            temporal_anomalies = np.zeros(len(df))
            
            # Map back to original indices
            df_with_time_indices = df_with_time.index.tolist()
            time_diff_indices = df_with_time_indices[1:]  # time_diffs starts from second entry
            
            for i, is_anomaly in enumerate(anomalous_time_diffs):
                if i < len(time_diff_indices):
                    original_idx = df.index.get_loc(time_diff_indices[i])
                    temporal_anomalies[original_idx] = float(is_anomaly)
            
            return temporal_anomalies
            
        except Exception as e:
            return np.zeros(len(df))
    
    def _detect_severity_anomalies(self, df):
        """
        Detect anomalies based on severity patterns
        """
        try:
            severity_counts = df['severity'].value_counts()
            total_logs = len(df)
            
            # Calculate severity frequencies
            severity_frequencies = severity_counts / total_logs
            
            # Define expected frequency ranges for different severities
            expected_ranges = {
                'ERROR': (0.001, 0.1),    # 0.1% to 10%
                'FATAL': (0.0001, 0.05),  # 0.01% to 5%
                'WARNING': (0.01, 0.3),   # 1% to 30%
                'INFO': (0.3, 0.95),      # 30% to 95%
                'DEBUG': (0.0, 0.5),      # 0% to 50%
            }
            
            # Identify anomalous severities
            severity_anomalies = np.zeros(len(df))
            
            for severity, (min_freq, max_freq) in expected_ranges.items():
                if severity in severity_frequencies:
                    freq = severity_frequencies[severity]
                    if freq < min_freq or freq > max_freq:
                        # Mark all entries of this severity as potentially anomalous
                        severity_mask = df['severity'] == severity
                        severity_anomalies[severity_mask] = 0.5  # Moderate anomaly score
            
            # Also mark rare severities as anomalous
            rare_severities = severity_frequencies[severity_frequencies < 0.01].index
            for severity in rare_severities:
                severity_mask = df['severity'] == severity
                severity_anomalies[severity_mask] = 1.0  # High anomaly score
            
            return severity_anomalies
            
        except Exception as e:
            return np.zeros(len(df))
    
    def _detect_pattern_anomalies(self, df):
        """
        Detect anomalies based on unusual patterns in log messages
        """
        try:
            messages = df['message'].fillna('').astype(str)
            pattern_anomalies = np.zeros(len(df))
            
            # Check for various suspicious patterns
            suspicious_patterns = [
                r'failed.*login',           # Failed login attempts
                r'unauthorized.*access',    # Unauthorized access
                r'connection.*refused',     # Connection issues
                r'timeout.*exceeded',       # Timeout issues
                r'memory.*leak',           # Memory issues
                r'stack.*overflow',        # Stack overflow
                r'null.*pointer',          # Null pointer exceptions
                r'out.*of.*memory',        # Memory exhaustion
                r'deadlock.*detected',     # Deadlock issues
                r'permission.*denied',     # Permission issues
            ]
            
            for i, message in enumerate(messages):
                message_lower = message.lower()
                
                # Check for suspicious patterns
                for pattern in suspicious_patterns:
                    if re.search(pattern, message_lower):
                        pattern_anomalies[i] = max(pattern_anomalies[i], 0.7)
                
                # Check for unusual characters or extremely long messages
                if len(message) > 1000:  # Very long message
                    pattern_anomalies[i] = max(pattern_anomalies[i], 0.3)
                
                # Check for messages with unusual character patterns
                if re.search(r'[^\x00-\x7F]', message):  # Non-ASCII characters
                    pattern_anomalies[i] = max(pattern_anomalies[i], 0.2)
                
                # Check for repeated characters (might indicate errors)
                if re.search(r'(.)\1{10,}', message):  # 10+ repeated characters
                    pattern_anomalies[i] = max(pattern_anomalies[i], 0.4)
            
            return pattern_anomalies
            
        except Exception as e:
            return np.zeros(len(df))
    
    def _combine_anomaly_scores(self, anomaly_scores, df):
        """
        Combine multiple anomaly detection methods using ensemble approach
        """
        try:
            if not anomaly_scores:
                return []
            
            # Stack all anomaly scores
            combined_scores = np.column_stack(anomaly_scores)
            
            # Calculate weighted average (you can adjust weights based on importance)
            weights = np.array([0.2, 0.25, 0.2, 0.15, 0.2])  # Adjust as needed
            weights = weights[:combined_scores.shape[1]]  # Match number of methods
            weights = weights / weights.sum()  # Normalize
            
            final_scores = np.average(combined_scores, axis=1, weights=weights)
            
            # Set threshold for anomaly detection
            threshold = 0.3  # Adjust based on desired sensitivity
            anomaly_indices = np.where(final_scores > threshold)[0].tolist()
            
            # Additional filtering: limit to top anomalies if too many detected
            if len(anomaly_indices) > len(df) * 0.2:  # Max 20% of logs as anomalies
                top_anomaly_indices = np.argsort(final_scores)[-int(len(df) * 0.2):]
                anomaly_indices = top_anomaly_indices.tolist()
            
            return anomaly_indices
            
        except Exception as e:
            return []
    
    def _clean_message(self, message):
        """
        Clean log message for text analysis
        """
        if not isinstance(message, str):
            return ""
        
        # Remove timestamps, IPs, numbers, and other noise
        cleaned = re.sub(r'\d{4}-\d{2}-\d{2}', '', message)  # Remove dates
        cleaned = re.sub(r'\d{2}:\d{2}:\d{2}', '', cleaned)  # Remove times
        cleaned = re.sub(r'\b\d+\.\d+\.\d+\.\d+\b', '', cleaned)  # Remove IPs
        cleaned = re.sub(r'\b\d+\b', '', cleaned)  # Remove standalone numbers
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)  # Remove special characters
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
        
        return cleaned.strip().lower()
    
    def get_anomaly_summary(self, df, anomaly_indices):
        """
        Generate a summary of detected anomalies
        """
        if not anomaly_indices or df.empty:
            return {
                'total_anomalies': 0,
                'anomaly_rate': 0,
                'severity_distribution': {},
                'common_patterns': []
            }
        
        anomaly_df = df.iloc[anomaly_indices]
        
        summary = {
            'total_anomalies': len(anomaly_indices),
            'anomaly_rate': len(anomaly_indices) / len(df) * 100,
            'severity_distribution': anomaly_df['severity'].value_counts().to_dict(),
            'common_patterns': self._find_common_patterns(anomaly_df['message']),
            'time_distribution': self._analyze_temporal_distribution(anomaly_df) if 'timestamp' in anomaly_df.columns else {}
        }
        
        return summary
    
    def _find_common_patterns(self, messages, top_n=5):
        """
        Find common patterns in anomalous messages
        """
        try:
            # Simple pattern extraction (you can enhance this)
            patterns = {}
            for message in messages:
                words = str(message).lower().split()
                for word in words:
                    if len(word) > 3:  # Only consider meaningful words
                        patterns[word] = patterns.get(word, 0) + 1
            
            # Return top patterns
            sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
            return sorted_patterns[:top_n]
            
        except Exception:
            return []
    
    def _analyze_temporal_distribution(self, anomaly_df):
        """
        Analyze temporal distribution of anomalies
        """
        try:
            if 'timestamp' not in anomaly_df.columns or anomaly_df['timestamp'].isna().all():
                return {}
            
            valid_timestamps = anomaly_df['timestamp'].dropna()
            if len(valid_timestamps) == 0:
                return {}
            
            return {
                'earliest_anomaly': valid_timestamps.min().isoformat(),
                'latest_anomaly': valid_timestamps.max().isoformat(),
                'anomaly_span_hours': (valid_timestamps.max() - valid_timestamps.min()).total_seconds() / 3600
            }
            
        except Exception:
            return {}
