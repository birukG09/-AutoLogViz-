import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class LogVisualizer:
    """
    Advanced visualization engine for log analysis
    """
    
    def __init__(self):
        # Color scheme for different severities
        self.severity_colors = {
            'FATAL': '#d32f2f',     # Red
            'ERROR': '#f57c00',     # Orange
            'WARNING': '#fbc02d',   # Yellow
            'INFO': '#388e3c',      # Green
            'DEBUG': '#1976d2',     # Blue
            'TRACE': '#7b1fa2'      # Purple
        }
        
        # Default color for unknown severities
        self.default_color = '#757575'  # Gray
    
    def create_timeline_chart(self, df):
        """
        Create an interactive timeline chart showing log entries over time
        """
        if 'timestamp' not in df.columns or df['timestamp'].isna().all():
            # Create a simple count chart if no timestamps
            return self._create_count_chart(df)
        
        # Filter out rows without timestamps
        df_with_time = df[df['timestamp'].notna()].copy()
        
        if df_with_time.empty:
            return self._create_empty_chart("No timestamp data available")
        
        # Aggregate by time intervals
        df_with_time['hour'] = df_with_time['timestamp'].dt.floor('h')
        
        # Count entries by hour and severity
        timeline_data = df_with_time.groupby(['hour', 'severity']).size().reset_index(name='count')
        
        # Create the timeline chart
        fig = px.line(
            timeline_data,
            x='hour',
            y='count',
            color='severity',
            color_discrete_map=self.severity_colors,
            title='Log Entries Timeline',
            labels={'hour': 'Time', 'count': 'Number of Log Entries'},
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Number of Log Entries",
            hovermode='x unified',
            legend_title="Severity Level"
        )
        
        return fig
    
    def create_severity_pie_chart(self, df):
        """
        Create a pie chart showing severity distribution
        """
        severity_counts = df['severity'].value_counts()
        
        if severity_counts.empty:
            return self._create_empty_chart("No severity data available")
        
        colors = [self.severity_colors.get(severity, self.default_color) 
                 for severity in severity_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=severity_counts.index,
            values=severity_counts.values,
            marker_colors=colors,
            textinfo='label+percent+value',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>' +
                         'Count: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title="Log Severity Distribution",
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
        
        return fig
    
    def create_severity_bar_chart(self, df):
        """
        Create a bar chart showing severity counts
        """
        severity_counts = df['severity'].value_counts()
        
        if severity_counts.empty:
            return self._create_empty_chart("No severity data available")
        
        colors = [self.severity_colors.get(severity, self.default_color) 
                 for severity in severity_counts.index]
        
        fig = go.Figure(data=[go.Bar(
            x=severity_counts.index,
            y=severity_counts.values,
            marker_color=colors,
            text=severity_counts.values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>' +
                         'Count: %{y}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title="Log Severity Counts",
            xaxis_title="Severity Level",
            yaxis_title="Number of Log Entries",
            showlegend=False
        )
        
        return fig
    
    def create_source_analysis_chart(self, df):
        """
        Create a chart analyzing log entries by source
        """
        if 'source' not in df.columns:
            return self._create_empty_chart("No source data available")
        
        source_counts = df['source'].value_counts().head(20)  # Top 20 sources
        
        if source_counts.empty:
            return self._create_empty_chart("No source data available")
        
        fig = go.Figure(data=[go.Bar(
            x=source_counts.values,
            y=source_counts.index,
            orientation='h',
            marker_color='lightblue',
            text=source_counts.values,
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>' +
                         'Count: %{x}<br>' +
                         '<extra></extra>'
        )])
        
        fig.update_layout(
            title="Top Log Sources",
            xaxis_title="Number of Log Entries",
            yaxis_title="Source",
            height=max(400, len(source_counts) * 25),
            showlegend=False
        )
        
        return fig
    
    def create_anomaly_chart(self, df, anomaly_indices):
        """
        Create a chart highlighting anomalies in the timeline
        """
        if 'timestamp' not in df.columns or df['timestamp'].isna().all():
            return self._create_empty_chart("No timestamp data for anomaly visualization")
        
        if not anomaly_indices:
            return self._create_empty_chart("No anomalies detected")
        
        # Filter data with timestamps
        df_with_time = df[df['timestamp'].notna()].copy()
        
        if df_with_time.empty:
            return self._create_empty_chart("No timestamp data available")
        
        # Aggregate by time intervals
        df_with_time['hour'] = df_with_time['timestamp'].dt.floor('h')
        hourly_counts = df_with_time.groupby('hour').size().reset_index(name='count')
        
        # Mark anomalies
        anomaly_df = df.iloc[anomaly_indices]
        anomaly_df_with_time = anomaly_df[anomaly_df['timestamp'].notna()].copy()
        
        if not anomaly_df_with_time.empty:
            anomaly_df_with_time['hour'] = anomaly_df_with_time['timestamp'].dt.floor('h')
            anomaly_hourly = anomaly_df_with_time.groupby('hour').size().reset_index(name='anomaly_count')
        else:
            anomaly_hourly = pd.DataFrame(columns=['hour', 'anomaly_count'])
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Normal Log Activity', 'Anomalies Detected'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Add normal activity
        fig.add_trace(
            go.Scatter(
                x=hourly_counts['hour'],
                y=hourly_counts['count'],
                mode='lines+markers',
                name='Log Count',
                line=dict(color='blue'),
                hovertemplate='Time: %{x}<br>Count: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add anomalies
        if not anomaly_hourly.empty:
            fig.add_trace(
                go.Scatter(
                    x=anomaly_hourly['hour'],
                    y=anomaly_hourly['anomaly_count'],
                    mode='markers',
                    name='Anomalies',
                    marker=dict(color='red', size=10),
                    hovertemplate='Time: %{x}<br>Anomalies: %{y}<extra></extra>'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title="Log Activity with Anomaly Detection",
            height=600,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Log Count", row=1, col=1)
        fig.update_yaxes(title_text="Anomaly Count", row=2, col=1)
        
        return fig
    
    def create_message_length_distribution(self, df):
        """
        Create a histogram showing message length distribution
        """
        if 'message_length' not in df.columns:
            return self._create_empty_chart("No message length data available")
        
        fig = px.histogram(
            df,
            x='message_length',
            title='Message Length Distribution',
            labels={'message_length': 'Message Length (characters)', 'count': 'Frequency'},
            nbins=50
        )
        
        fig.update_layout(
            xaxis_title="Message Length (characters)",
            yaxis_title="Frequency",
            showlegend=False
        )
        
        return fig
    
    def create_heatmap(self, df):
        """
        Create a heatmap showing log activity patterns
        """
        if 'timestamp' not in df.columns or df['timestamp'].isna().all():
            return self._create_empty_chart("No timestamp data for heatmap")
        
        df_with_time = df[df['timestamp'].notna()].copy()
        
        if df_with_time.empty:
            return self._create_empty_chart("No timestamp data available")
        
        # Extract hour and day of week
        df_with_time['hour'] = df_with_time['timestamp'].dt.hour
        df_with_time['day_of_week'] = df_with_time['timestamp'].dt.day_name()
        
        # Create pivot table for heatmap
        heatmap_data = df_with_time.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='day_of_week', columns='hour', values='count').fillna(0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex([day for day in day_order if day in heatmap_pivot.index])
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='Viridis',
            hovertemplate='Day: %{y}<br>Hour: %{x}<br>Count: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Log Activity Heatmap (Day vs Hour)",
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week"
        )
        
        return fig
    
    def _create_count_chart(self, df):
        """
        Create a simple count chart when timestamps are not available
        """
        fig = go.Figure(data=[go.Bar(
            x=['Total Log Entries'],
            y=[len(df)],
            marker_color='lightblue',
            text=[len(df)],
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Total Log Entries",
            xaxis_title="",
            yaxis_title="Count",
            showlegend=False
        )
        
        return fig
    
    def _create_empty_chart(self, message):
        """
        Create an empty chart with a message
        """
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        
        fig.update_layout(
            title="No Data Available",
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            height=400
        )
        
        return fig
    
    def create_severity_timeline(self, df):
        """
        Create a stacked area chart showing severity distribution over time
        """
        if 'timestamp' not in df.columns or df['timestamp'].isna().all():
            return self._create_empty_chart("No timestamp data available")
        
        df_with_time = df[df['timestamp'].notna()].copy()
        
        if df_with_time.empty:
            return self._create_empty_chart("No timestamp data available")
        
        # Aggregate by time intervals and severity
        df_with_time['hour'] = df_with_time['timestamp'].dt.floor('h')
        severity_timeline = df_with_time.groupby(['hour', 'severity']).size().reset_index(name='count')
        
        # Pivot for stacked area chart
        severity_pivot = severity_timeline.pivot(index='hour', columns='severity', values='count').fillna(0)
        
        fig = go.Figure()
        
        for severity in severity_pivot.columns:
            color = self.severity_colors.get(severity, self.default_color)
            fig.add_trace(go.Scatter(
                x=severity_pivot.index,
                y=severity_pivot[severity],
                mode='lines',
                stackgroup='one',
                name=severity,
                fill='tonexty',
                line=dict(color=color),
                hovertemplate=f'<b>{severity}</b><br>Time: %{{x}}<br>Count: %{{y}}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Severity Distribution Over Time",
            xaxis_title="Time",
            yaxis_title="Number of Log Entries",
            hovermode='x unified'
        )
        
        return fig
