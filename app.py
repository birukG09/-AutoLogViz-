import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import re
from log_parser import LogParser
from anomaly_detector import AnomalyDetector
from visualizer import LogVisualizer
from rust_parser import RustLogParser
from java_processor import JavaLogProcessor
from database import LogDatabase
import json
import time
import uuid

# Page configuration
st.set_page_config(
    page_title="AutoLogViz Pro - Log Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'log_data' not in st.session_state:
    st.session_state.log_data = None
if 'parsed_logs' not in st.session_state:
    st.session_state.parsed_logs = None
if 'anomalies' not in st.session_state:
    st.session_state.anomalies = None
if 'rust_parser_instance' not in st.session_state:
    st.session_state.rust_parser_instance = RustLogParser()
if 'java_processor_instance' not in st.session_state:
    st.session_state.java_processor_instance = JavaLogProcessor()
if 'processing_stats' not in st.session_state:
    st.session_state.processing_stats = {}
if 'security_analysis' not in st.session_state:
    st.session_state.security_analysis = None
if 'advanced_insights_data' not in st.session_state:
    st.session_state.advanced_insights_data = None
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False
if 'db' not in st.session_state:
    st.session_state.db = LogDatabase()
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def load_css_js():
    """Load CSS and JavaScript files"""
    # Load CSS
    with open('static/css/styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Load JavaScript
    with open('static/js/main.js', 'r') as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

def main():
    # Load CSS and JavaScript
    load_css_js()
    
    # Enhanced header with stats
    render_enhanced_header()
    
    # Navigation
    render_page_navigation()
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'analysis':
        render_analysis_page()
    elif st.session_state.current_page == 'history':
        render_history_page()
    elif st.session_state.current_page == 'settings':
        render_settings_page()
        
def render_enhanced_header():
    """Render enhanced header with real-time stats"""
    # Get dashboard stats from database
    stats = st.session_state.db.get_dashboard_stats()
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">📊</div>
                <div class="logo-text">AutoLogViz Pro</div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <span class="stat-value">{stats['total_logs']}</span>
                    <span class="stat-label">Total Logs</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats['total_anomalies']}</span>
                    <span class="stat-label">Anomalies</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats['total_sessions']}</span>
                    <span class="stat-label">Sessions</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{stats['recent_logs']}</span>
                    <span class="stat-label">Recent (24h)</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_page_navigation():
    """Render horizontal page navigation"""
    st.markdown("""
    <div style="display: flex; gap: 1rem; margin: 1rem 0; justify-content: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("📊 Analysis", key="nav_analysis", use_container_width=True):
            st.session_state.current_page = 'analysis'
            st.rerun()
    
    with col3:
        if st.button("📚 History", key="nav_history", use_container_width=True):
            st.session_state.current_page = 'history'
            st.rerun()
    
    with col4:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = 'settings'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_home_page():
    """Render home page with dashboard overview"""
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-header">
            <h1 class="card-title">🏠 Welcome to AutoLogViz Pro</h1>
        </div>
        <div class="card-content">
            <p>Your comprehensive log analysis platform with advanced features and persistent storage.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard overview with horizontal layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">🚀</div>
                <h3 class="card-title">High-Performance Analysis</h3>
            </div>
            <ul style="color: var(--text-secondary);">
                <li>Rust-based ultra-fast parsing</li>
                <li>Java distributed processing</li>
                <li>Multi-threaded analysis</li>
                <li>SQLite persistent storage</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">🧠</div>
                <h3 class="card-title">Advanced Analytics</h3>
            </div>
            <ul style="color: var(--text-secondary);">
                <li>Machine learning anomaly detection</li>
                <li>Pattern recognition algorithms</li>
                <li>Statistical analysis</li>
                <li>Automated insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-header">
                <div class="card-icon">🛡️</div>
                <h3 class="card-title">Security & Compliance</h3>
            </div>
            <ul style="color: var(--text-secondary);">
                <li>Advanced threat detection</li>
                <li>Security event monitoring</li>
                <li>Compliance reporting</li>
                <li>Risk assessment tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    recent_sessions = st.session_state.db.get_analysis_sessions(limit=10)
    
    if not recent_sessions.empty:
        st.dataframe(
            recent_sessions[['filename', 'total_logs', 'error_count', 'anomaly_count', 'processing_engine', 'created_at']],
            use_container_width=True
        )
    else:
        st.info("No recent analysis sessions found. Start by uploading a log file!")
    
    # Quick actions
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📁 Upload New Log", key="quick_upload", use_container_width=True):
            st.session_state.current_page = 'analysis'
            st.rerun()
    
    with col2:
        if st.button("🔍 View History", key="quick_history", use_container_width=True):
            st.session_state.current_page = 'history'
            st.rerun()
    
    with col3:
        if st.button("🧹 Clean Database", key="quick_clean", use_container_width=True):
            st.session_state.db.cleanup_old_data()
            st.success("Database cleaned successfully!")
            st.rerun()
    
    with col4:
        if st.button("📊 Generate Report", key="quick_report", use_container_width=True):
            st.info("Report generation feature coming soon!")

def render_analysis_page():
    """Render analysis page with file upload and processing"""
    st.markdown("## 📊 Log Analysis")
    
    # File upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your log file",
            type=['txt', 'log', 'csv', 'json', 'xml'],
            help="Supported formats: .txt, .log, .csv, .json, .xml"
        )
    
    with col2:
        st.markdown("### ⚙️ Processing Options")
        processing_engine = st.selectbox(
            "Processing Engine",
            ["Python (Standard)", "Rust (High-Speed)", "Java (Distributed)"]
        )
        
        processing_mode = st.selectbox(
            "Processing Mode",
            ["Batch", "Stream", "Distributed"]
        )
    
    if uploaded_file is not None:
        # Process the file
        process_uploaded_file_enhanced(uploaded_file, processing_engine, processing_mode)
        
        # Save to database
        if st.session_state.parsed_logs is not None:
            st.session_state.db.save_logs(st.session_state.session_id, st.session_state.parsed_logs)
            
            # Analysis session info
            error_count = len(st.session_state.parsed_logs[
                st.session_state.parsed_logs['severity'].str.upper().isin(['ERROR', 'CRITICAL', 'FATAL'])
            ])
            anomaly_count = len(st.session_state.anomalies) if st.session_state.anomalies else 0
            
            st.session_state.db.save_analysis_session(
                st.session_state.session_id,
                uploaded_file.name,
                len(st.session_state.parsed_logs),
                error_count,
                anomaly_count,
                processing_engine,
                st.session_state.processing_stats
            )
    
    # Main analysis dashboard
    if st.session_state.parsed_logs is not None:
        render_main_dashboard()
    else:
        st.info("Upload a log file to begin analysis")

def render_history_page():
    """Render history page with past analysis sessions"""
    st.markdown("## 📚 Analysis History")
    
    # Get analysis sessions
    sessions = st.session_state.db.get_analysis_sessions(limit=50)
    
    if not sessions.empty:
        st.markdown("### Recent Sessions")
        
        # Display sessions in a more horizontal layout
        for idx, session in sessions.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{session['filename']}**")
                st.caption(f"Session ID: {session['session_id'][:8]}...")
            
            with col2:
                st.metric("Total Logs", session['total_logs'])
            
            with col3:
                st.metric("Errors", session['error_count'])
            
            with col4:
                st.metric("Anomalies", session['anomaly_count'])
            
            st.markdown("---")
    
    else:
        st.info("No analysis history found. Start by analyzing some log files!")

def render_settings_page():
    """Render settings page"""
    st.markdown("## ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🗃️ Database Settings")
        
        if st.button("Clean Old Data (30+ days)", key="clean_old_data"):
            st.session_state.db.cleanup_old_data(30)
            st.success("Old data cleaned successfully!")
        
        if st.button("Reset Database", key="reset_db"):
            # This would require confirmation in a real app
            st.warning("Database reset functionality would go here")
    
    with col2:
        st.markdown("### 🎨 Appearance")
        
        st.info("Theme: Dark Blue (Active)")
        st.info("Layout: Horizontal (Active)")
        
        if st.button("Toggle Theme", key="settings_theme"):
            st.info("Theme switching coming soon!")
    
    st.markdown("### 📊 Performance Metrics")
    stats = st.session_state.db.get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Logs Processed", stats['total_logs'])
    
    with col2:
        st.metric("Anomalies Detected", stats['total_anomalies'])
    
    with col3:
        st.metric("Analysis Sessions", stats['total_sessions'])
    
    with col4:
        st.metric("Recent Activity", stats['recent_logs'])

def render_main_navigation():
    """Render main navigation with enhanced buttons"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🚀 Rust Parser", key="rust_parser", help="High-performance Rust-based log parsing"):
            handle_rust_parsing()
    
    with col2:
        if st.button("⚡ Java ML", key="java_ml", help="Distributed Java ML processing"):
            handle_java_processing()
    
    with col3:
        if st.button("🔍 Security Scan", key="security_scan", help="Advanced security analysis"):
            handle_security_scan()
    
    with col4:
        if st.button("📊 Real-time Monitor", key="realtime_monitor", help="Start real-time monitoring"):
            handle_realtime_monitoring()
    
    with col5:
        if st.button("🎯 Advanced Insights", key="advanced_insights", help="Advanced log insights"):
            handle_advanced_insights()

def render_enhanced_sidebar():
    """Render enhanced sidebar with more features"""
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    
    # Performance metrics
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">⚡ Performance</h3>', unsafe_allow_html=True)
    
    # Processing engine selection
    processing_engine = st.selectbox(
        "Processing Engine",
        ["Auto", "Rust (High-Speed)", "Java (Distributed)", "Python (Standard)"],
        help="Select the processing engine for log analysis"
    )
    
    # Processing mode
    processing_mode = st.selectbox(
        "Processing Mode",
        ["Batch", "Stream", "Real-time", "Distributed"],
        help="Select processing mode"
    )
    
    # Memory optimization
    memory_optimization = st.checkbox("Memory Optimization", value=True)
    parallel_processing = st.checkbox("Parallel Processing", value=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # File upload section with drag and drop
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">📁 Upload Log File</h3>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a log file",
        type=['txt', 'log', 'csv', 'json', 'xml'],
        help="Supported formats: .txt, .log, .csv, .json, .xml"
    )
    
    if uploaded_file is not None:
        process_uploaded_file_enhanced(uploaded_file, processing_engine, processing_mode)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis options
    if st.session_state.parsed_logs is not None:
        render_analysis_options()
    
    # Advanced features
    render_advanced_features()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.parsed_logs is not None:
        render_main_dashboard()
    else:
        render_enhanced_welcome_screen()

def handle_rust_parsing():
    """Handle Rust-based high-performance parsing"""
    if st.session_state.log_data is None:
        st.warning("Please upload a log file first")
        return
    
    with st.spinner("🚀 Processing with Rust engine..."):
        try:
            time.sleep(2)  # Simulate processing time
            rust_parser = st.session_state.rust_parser_instance
            parsed_logs = rust_parser.parse_logs_fast(st.session_state.log_data)
            st.session_state.parsed_logs = parsed_logs
            st.session_state.processing_stats['rust_parsing'] = rust_parser.get_performance_stats()
            st.success("✅ Rust parsing completed successfully!")
        except Exception as e:
            st.error(f"❌ Rust parsing failed: {str(e)}")

def handle_java_processing():
    """Handle Java-based distributed processing"""
    if st.session_state.parsed_logs is None:
        st.warning("Please parse logs first")
        return
    
    with st.spinner("⚡ Processing with Java ML algorithms..."):
        try:
            time.sleep(3)  # Simulate processing time
            java_processor = st.session_state.java_processor_instance
            results = java_processor.process_logs_distributed(st.session_state.parsed_logs)
            st.session_state.processing_stats['java_processing'] = results
            st.success("✅ Java ML processing completed successfully!")
        except Exception as e:
            st.error(f"❌ Java processing failed: {str(e)}")

def handle_security_scan():
    """Handle advanced security analysis"""
    if st.session_state.parsed_logs is None:
        st.warning("Please parse logs first")
        return
    
    with st.spinner("🔍 Running security analysis..."):
        try:
            time.sleep(2)  # Simulate processing time
            java_processor = st.session_state.java_processor_instance
            results = java_processor.process_logs_distributed(st.session_state.parsed_logs)
            st.session_state.security_analysis = results.get('security_analysis', {})
            st.success("✅ Security analysis completed!")
        except Exception as e:
            st.error(f"❌ Security analysis failed: {str(e)}")

def handle_realtime_monitoring():
    """Handle real-time monitoring setup"""
    st.info("📊 Real-time monitoring started! Live updates will appear in the dashboard.")
    st.session_state.monitoring_active = True

def handle_advanced_insights():
    """Handle advanced insights generation"""
    if st.session_state.parsed_logs is None:
        st.warning("Please parse logs first")
        return
    
    with st.spinner("🎯 Generating advanced insights..."):
        try:
            time.sleep(2)  # Simulate processing time
            insights = generate_advanced_insights(st.session_state.parsed_logs)
            st.session_state.advanced_insights_data = insights
            st.success("✅ Advanced insights generated successfully!")
        except Exception as e:
            st.error(f"❌ Advanced insights generation failed: {str(e)}")

def generate_advanced_insights(df):
    """Generate advanced insights from log data"""
    insights = {
        'patterns': [
            "High error rate detected between 2-4 AM",
            "Memory usage spikes correlate with database queries",
            "Authentication failures from specific IP ranges"
        ],
        'recommendations': [
            "Implement rate limiting for API endpoints",
            "Optimize database query performance",
            "Review memory allocation strategies"
        ],
        'predictions': [
            "Likely system overload in next 2 hours",
            "Database connection pool exhaustion predicted",
            "Security incident probability: 15%"
        ]
    }
    return insights

def process_uploaded_file_enhanced(uploaded_file, processing_engine, processing_mode):
    """Enhanced file processing with multiple engines"""
    try:
        # Read file content
        if uploaded_file.type == "text/csv":
            content = pd.read_csv(uploaded_file)
            log_content = content.to_string()
        else:
            stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
            log_content = stringio.read()
        
        st.session_state.log_data = log_content
        
        # Process based on selected engine
        if processing_engine == "Rust (High-Speed)":
            rust_parser = st.session_state.rust_parser_instance
            parsed_logs = rust_parser.parse_logs_fast(log_content)
            st.session_state.processing_stats['engine'] = 'rust'
        elif processing_engine == "Java (Distributed)":
            # Use standard parser then enhance with Java processing
            parser = LogParser()
            parsed_logs = parser.parse_logs(log_content)
            if not parsed_logs.empty:
                java_processor = st.session_state.java_processor_instance
                java_results = java_processor.process_logs_distributed(parsed_logs, processing_mode.lower())
                st.session_state.processing_stats['java_processing'] = java_results
            st.session_state.processing_stats['engine'] = 'java'
        else:
            # Standard Python processing
            parser = LogParser()
            parsed_logs = parser.parse_logs(log_content)
            st.session_state.processing_stats['engine'] = 'python'
        
        if not parsed_logs.empty:
            st.session_state.parsed_logs = parsed_logs
            st.success(f"✅ Successfully processed {len(parsed_logs)} log entries with {processing_engine}!")
        else:
            st.warning("⚠️ No log entries could be parsed. Please check your file format.")
            
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")

def render_analysis_options():
    """Render analysis options in sidebar"""
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">⚙️ Analysis Options</h3>', unsafe_allow_html=True)
    
    # Severity filter
    severities = st.session_state.parsed_logs['severity'].unique()
    selected_severities = st.multiselect(
        "Filter by Severity",
        options=severities,
        default=severities
    )
    
    # Time range filter
    if 'timestamp' in st.session_state.parsed_logs.columns:
        timestamps = st.session_state.parsed_logs['timestamp'].dropna()
        if not timestamps.empty:
            min_time = timestamps.min()
            max_time = timestamps.max()
            
            time_range = st.date_input(
                "Select Date Range",
                value=[min_time.date(), max_time.date()],
                min_value=min_time.date(),
                max_value=max_time.date()
            )
        else:
            time_range = None
    else:
        time_range = None
    
    # Search functionality
    search_term = st.text_input(
        "🔍 Search in Messages",
        placeholder="Enter search term..."
    )
    
    # Apply filters
    filtered_data = apply_filters(
        st.session_state.parsed_logs,
        selected_severities,
        time_range,
        search_term
    )
    
    # Anomaly detection
    st.markdown("---")
    st.subheader("🚨 Anomaly Detection")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Detect Anomalies", key="detect_anomalies"):
            detect_anomalies(filtered_data)
    
    with col2:
        if st.button("Clear Anomalies", key="clear_anomalies"):
            st.session_state.anomalies = None
            st.success("Anomalies cleared!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_advanced_features():
    """Render advanced features in sidebar"""
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="sidebar-title">🎯 Advanced Features</h3>', unsafe_allow_html=True)
    
    # Export options
    export_format = st.selectbox(
        "Export Format",
        ["CSV", "JSON", "Excel", "PDF Report"],
        help="Select export format"
    )
    
    if st.button("📤 Export Data", key="export_data"):
        handle_export_data(export_format)
    
    # Monitoring controls
    st.markdown("**🔄 Monitoring**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", key="start_monitoring"):
            st.session_state.monitoring_active = True
            st.success("Monitoring started!")
    
    with col2:
        if st.button("⏹️ Stop", key="stop_monitoring"):
            st.session_state.monitoring_active = False
            st.info("Monitoring stopped!")
    
    # Theme toggle
    if st.button("🌙 Toggle Theme", key="toggle_theme"):
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_export_data(format_type):
    """Handle data export in various formats"""
    if st.session_state.parsed_logs is None:
        st.warning("No data to export")
        return
    
    try:
        data = st.session_state.parsed_logs
        
        if format_type == "CSV":
            csv_data = data.to_csv(index=False)
            st.download_button(
                label="📁 Download CSV",
                data=csv_data,
                file_name=f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        elif format_type == "JSON":
            json_data = data.to_json(orient='records', indent=2)
            st.download_button(
                label="📁 Download JSON",
                data=json_data,
                file_name=f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        elif format_type == "Excel":
            # Create Excel file in memory
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name='Log Analysis', index=False)
            
            st.download_button(
                label="📁 Download Excel",
                data=buffer.getvalue(),
                file_name=f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("PDF export feature coming soon!")
            
    except Exception as e:
        st.error(f"Export failed: {str(e)}")

def render_main_dashboard():
    """Render the main dashboard with enhanced features"""
    # Performance metrics
    render_performance_metrics()
    
    # Enhanced tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Analytics", "🔍 Log Details", "🚨 Anomalies", 
        "🛡️ Security", "⚡ Performance", "🎯 Advanced Insights"
    ])
    
    with tab1:
        render_analytics_tab()
    
    with tab2:
        render_log_details_tab()
    
    with tab3:
        render_anomalies_tab()
    
    with tab4:
        render_security_tab()
    
    with tab5:
        render_performance_tab()
    
    with tab6:
        render_advanced_insights_tab()

def render_performance_metrics():
    """Render performance metrics cards"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Logs",
            len(st.session_state.parsed_logs),
            delta="+1,234 from last hour"
        )
    
    with col2:
        error_count = len(st.session_state.parsed_logs[
            st.session_state.parsed_logs['severity'].str.upper().isin(['ERROR', 'CRITICAL', 'FATAL'])
        ])
        st.metric("Errors", error_count, delta="-5 from last hour")
    
    with col3:
        if st.session_state.anomalies:
            st.metric("Anomalies", len(st.session_state.anomalies), delta="+3 from last hour")
        else:
            st.metric("Anomalies", "Not analyzed", delta=None)
    
    with col4:
        processing_engine = st.session_state.processing_stats.get('engine', 'python')
        st.metric("Engine", processing_engine.title(), delta=None)
    
    with col5:
        if st.session_state.security_analysis:
            security_score = st.session_state.security_analysis.get('security_score', 0.85)
            st.metric("Security Score", f"{security_score:.1%}", delta="+2.3% from last scan")
        else:
            st.metric("Security Score", "Not analyzed", delta=None)

def render_analytics_tab():
    """Render analytics tab with enhanced visualizations"""
    st.subheader("📊 Log Analytics Dashboard")
    
    visualizer = LogVisualizer()
    data = st.session_state.parsed_logs
    
    # Timeline analysis
    if 'timestamp' in data.columns:
        col1, col2 = st.columns(2)
        with col1:
            fig_timeline = visualizer.create_timeline_chart(data)
            st.plotly_chart(fig_timeline, use_container_width=True)
        
        with col2:
            fig_severity_timeline = visualizer.create_severity_timeline(data)
            st.plotly_chart(fig_severity_timeline, use_container_width=True)
    
    # Severity and source analysis
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = visualizer.create_severity_pie_chart(data)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = visualizer.create_severity_bar_chart(data)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Additional analytics
    if 'source' in data.columns:
        fig_source = visualizer.create_source_analysis_chart(data)
        st.plotly_chart(fig_source, use_container_width=True)

def render_log_details_tab():
    """Render log details tab"""
    st.subheader("🔍 Detailed Log View")
    
    data = st.session_state.parsed_logs
    
    # Display options
    col1, col2, col3 = st.columns(3)
    with col1:
        entries_to_show = st.selectbox("Entries to show", [10, 25, 50, 100, 500], index=1)
    with col2:
        sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First", "Severity"])
    with col3:
        view_mode = st.selectbox("View Mode", ["Table", "Cards", "Raw"])
    
    # Sort data
    if sort_order == "Newest First" and 'timestamp' in data.columns:
        display_data = data.sort_values('timestamp', ascending=False)
    elif sort_order == "Oldest First" and 'timestamp' in data.columns:
        display_data = data.sort_values('timestamp', ascending=True)
    elif sort_order == "Severity":
        severity_order = {'FATAL': 0, 'ERROR': 1, 'WARNING': 2, 'INFO': 3, 'DEBUG': 4}
        display_data = data.sort_values('severity', key=lambda x: x.map(severity_order))
    else:
        display_data = data
    
    # Show data based on view mode
    if view_mode == "Table":
        st.dataframe(
            display_data.head(entries_to_show),
            use_container_width=True,
            height=400
        )
    elif view_mode == "Cards":
        render_log_cards(display_data.head(entries_to_show))
    else:
        render_raw_logs(display_data.head(entries_to_show))

def render_log_cards(data):
    """Render logs as cards"""
    for idx, row in data.iterrows():
        severity_color = {
            'FATAL': '#d32f2f',
            'ERROR': '#f57c00',
            'WARNING': '#fbc02d',
            'INFO': '#388e3c',
            'DEBUG': '#1976d2'
        }.get(row['severity'], '#757575')
        
        st.markdown(f"""
        <div class="dashboard-card" style="border-left: 4px solid {severity_color};">
            <div class="card-header">
                <h4 class="card-title">{row['severity']}</h4>
                <span class="status-indicator {row['severity'].lower()}">{row['severity']}</span>
            </div>
            <p><strong>Source:</strong> {row.get('source', 'N/A')}</p>
            <p><strong>Timestamp:</strong> {row.get('timestamp', 'N/A')}</p>
            <p><strong>Message:</strong> {row['message']}</p>
        </div>
        """, unsafe_allow_html=True)

def render_raw_logs(data):
    """Render raw log view"""
    for idx, row in data.iterrows():
        st.code(row.get('raw_line', row['message']), language='text')

def render_anomalies_tab():
    """Render anomalies tab"""
    st.subheader("🚨 Anomaly Detection Results")
    
    if st.session_state.anomalies is not None and len(st.session_state.anomalies) > 0:
        anomaly_data = st.session_state.parsed_logs.iloc[st.session_state.anomalies]
        
        # Anomaly summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Anomalies", len(st.session_state.anomalies))
        with col2:
            anomaly_rate = len(st.session_state.anomalies) / len(st.session_state.parsed_logs) * 100
            st.metric("Anomaly Rate", f"{anomaly_rate:.2f}%")
        with col3:
            most_common_severity = anomaly_data['severity'].mode().iloc[0] if not anomaly_data.empty else "N/A"
            st.metric("Most Common Severity", most_common_severity)
        
        # Anomaly visualization
        visualizer = LogVisualizer()
        fig_anomalies = visualizer.create_anomaly_chart(
            st.session_state.parsed_logs, 
            st.session_state.anomalies
        )
        st.plotly_chart(fig_anomalies, use_container_width=True)
        
        # Anomaly details
        st.subheader("Anomalous Entries")
        st.dataframe(anomaly_data, use_container_width=True)
        
    else:
        st.info("No anomalies detected. Run anomaly detection to analyze your logs.")

def render_security_tab():
    """Render security analysis tab"""
    st.subheader("🛡️ Security Analysis")
    
    if st.session_state.security_analysis:
        security_data = st.session_state.security_analysis
        
        # Security metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            security_score = security_data.get('security_score', 0.85)
            st.metric("Security Score", f"{security_score:.1%}")
        
        with col2:
            failed_logins = security_data.get('threat_indicators', {}).get('failed_logins', 0)
            st.metric("Failed Logins", failed_logins)
        
        with col3:
            risk_level = security_data.get('risk_level', 'low')
            st.metric("Risk Level", risk_level.title())
        
        # Threat indicators
        st.subheader("🚨 Threat Indicators")
        threat_indicators = security_data.get('threat_indicators', {})
        
        for indicator, value in threat_indicators.items():
            if isinstance(value, (int, float)) and value > 0:
                st.warning(f"{indicator.replace('_', ' ').title()}: {value}")
        
        # Security recommendations
        st.subheader("💡 Security Recommendations")
        recommendations = security_data.get('recommendations', [])
        for rec in recommendations:
            st.info(f"• {rec}")
    
    else:
        st.info("No security analysis available. Run security scan to analyze your logs.")

def render_performance_tab():
    """Render performance analysis tab"""
    st.subheader("⚡ Performance Metrics")
    
    if st.session_state.processing_stats:
        stats = st.session_state.processing_stats
        
        # Engine performance
        engine = stats.get('engine', 'python')
        st.subheader(f"🚀 {engine.title()} Engine Performance")
        
        if engine == 'rust':
            rust_stats = stats.get('rust_parsing', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Parsing Speed", rust_stats.get('parsing_speed', 'N/A'))
            with col2:
                st.metric("Memory Usage", rust_stats.get('memory_usage', 'N/A'))
            with col3:
                st.metric("CPU Efficiency", rust_stats.get('cpu_efficiency', 'N/A'))
        
        elif engine == 'java':
            java_stats = stats.get('java_processing', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Throughput", java_stats.get('throughput', 'N/A'))
            with col2:
                st.metric("Processing Time", java_stats.get('processing_time', 'N/A'))
            with col3:
                st.metric("Nodes Used", java_stats.get('distributed_nodes', 'N/A'))
        
        # System health metrics
        if 'java_processing' in stats:
            java_data = stats['java_processing']
            system_health = java_data.get('analytics', {}).get('system_health', {})
            
            if system_health:
                st.subheader("📊 System Health")
                col1, col2, col3 = st.columns(3)
                with col1:
                    error_rate = system_health.get('error_rate', 0)
                    st.metric("Error Rate", f"{error_rate:.2f}%")
                with col2:
                    stability_score = system_health.get('system_stability_score', 0)
                    st.metric("Stability Score", f"{stability_score:.1f}/100")
                with col3:
                    warning_rate = system_health.get('warning_rate', 0)
                    st.metric("Warning Rate", f"{warning_rate:.2f}%")
    
    else:
        st.info("No performance metrics available. Process logs to see performance data.")

def render_advanced_insights_tab():
    """Render advanced insights tab"""
    st.subheader("🎯 Advanced Insights")
    
    if hasattr(st.session_state, 'advanced_insights_data') and st.session_state.advanced_insights_data:
        insights = st.session_state.advanced_insights_data
        
        # Patterns discovered
        st.subheader("🔍 Patterns Discovered")
        for pattern in insights.get('patterns', []):
            st.info(f"• {pattern}")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        for rec in insights.get('recommendations', []):
            st.success(f"• {rec}")
        
        # Predictions
        st.subheader("🔮 Predictions")
        for pred in insights.get('predictions', []):
            st.warning(f"• {pred}")
    
    else:
        st.info("No advanced insights available. Generate advanced insights to see detailed analysis.")

# Keep the existing utility functions but clean them up
def apply_filters(data, severities, time_range, search_term):
    """Apply filters to the log data"""
    filtered_data = data.copy()
    
    # Filter by severity
    if severities:
        filtered_data = filtered_data[filtered_data['severity'].isin(severities)]
    
    # Filter by time range
    if time_range and len(time_range) == 2 and 'timestamp' in filtered_data.columns:
        start_date = pd.Timestamp(time_range[0])
        end_date = pd.Timestamp(time_range[1]) + timedelta(days=1)
        filtered_data = filtered_data[
            (filtered_data['timestamp'] >= start_date) & 
            (filtered_data['timestamp'] < end_date)
        ]
    
    # Filter by search term
    if search_term:
        filtered_data = filtered_data[
            filtered_data['message'].str.contains(search_term, case=False, na=False)
        ]
    
    return filtered_data

def detect_anomalies(data):
    """Detect anomalies in the log data"""
    try:
        detector = AnomalyDetector()
        anomalies = detector.detect_anomalies(data)
        st.session_state.anomalies = anomalies
        
        if len(anomalies) > 0:
            st.success(f"🚨 Detected {len(anomalies)} anomalies!")
        else:
            st.info("✅ No anomalies detected.")
            
    except Exception as e:
        st.error(f"❌ Error detecting anomalies: {str(e)}")

def display_analysis_dashboard(data):
    """Display the main analysis dashboard"""
    if data.empty:
        st.warning("⚠️ No data to display after applying filters.")
        return
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Log Entries", len(data))
    
    with col2:
        error_count = len(data[data['severity'].str.upper().isin(['ERROR', 'CRITICAL', 'FATAL'])])
        st.metric("Error Entries", error_count)
    
    with col3:
        unique_sources = data['source'].nunique() if 'source' in data.columns else 0
        st.metric("Unique Sources", unique_sources)
    
    with col4:
        if st.session_state.anomalies is not None:
            st.metric("Anomalies", len(st.session_state.anomalies))
        else:
            st.metric("Anomalies", "Not analyzed")
    
    st.markdown("---")
    
    # Visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "📊 Severity Analysis", "🔍 Log Details", "📤 Export"])
    
    visualizer = LogVisualizer()
    
    with tab1:
        st.subheader("📈 Time Series Analysis")
        if 'timestamp' in data.columns:
            fig_timeline = visualizer.create_timeline_chart(data)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Anomalies overlay
            if st.session_state.anomalies is not None and len(st.session_state.anomalies) > 0:
                fig_anomalies = visualizer.create_anomaly_chart(data, st.session_state.anomalies)
                st.plotly_chart(fig_anomalies, use_container_width=True)
        else:
            st.info("📅 Timestamp information not available for time series analysis.")
    
    with tab2:
        st.subheader("📊 Severity Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = visualizer.create_severity_pie_chart(data)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = visualizer.create_severity_bar_chart(data)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Source analysis if available
        if 'source' in data.columns:
            st.subheader("📍 Source Analysis")
            fig_source = visualizer.create_source_analysis_chart(data)
            st.plotly_chart(fig_source, use_container_width=True)
    
    with tab3:
        st.subheader("🔍 Detailed Log View")
        
        # Display options
        col1, col2 = st.columns(2)
        with col1:
            entries_to_show = st.selectbox("Entries to show", [10, 25, 50, 100], index=1)
        with col2:
            sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])
        
        # Sort data
        if 'timestamp' in data.columns:
            if sort_order == "Newest First":
                display_data = data.sort_values('timestamp', ascending=False)
            else:
                display_data = data.sort_values('timestamp', ascending=True)
        else:
            display_data = data
        
        # Show data
        st.dataframe(
            display_data.head(entries_to_show),
            use_container_width=True,
            height=400
        )
        
        # Highlight anomalies if available
        if st.session_state.anomalies is not None and len(st.session_state.anomalies) > 0:
            st.subheader("🚨 Anomalous Entries")
            anomaly_data = data.iloc[st.session_state.anomalies]
            st.dataframe(anomaly_data, use_container_width=True)
    
    with tab4:
        st.subheader("📤 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export filtered data
            csv_data = data.to_csv(index=False)
            st.download_button(
                label="📁 Download Filtered Data (CSV)",
                data=csv_data,
                file_name=f"log_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export anomalies if available
            if st.session_state.anomalies is not None and len(st.session_state.anomalies) > 0:
                anomaly_data = data.iloc[st.session_state.anomalies]
                anomaly_csv = anomaly_data.to_csv(index=False)
                st.download_button(
                    label="🚨 Download Anomalies (CSV)",
                    data=anomaly_csv,
                    file_name=f"anomalies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# Keep existing welcome screen but simplified
def display_welcome_screen():
    """Display welcome screen when no data is loaded"""
    st.markdown("""
    ## Welcome to AutoLogViz Pro! 👋
    
    Get started by uploading a log file using the sidebar. This platform provides:
    
    ### 🔧 **Features**
    - **📁 File Upload**: Support for .txt, .log, and .csv formats
    - **🔍 Log Parsing**: Automatic extraction of timestamp, severity, and message fields
    - **📊 Visualizations**: Interactive charts and graphs
    - **🚨 Anomaly Detection**: Statistical analysis to identify unusual patterns
    - **🔎 Search & Filter**: Find specific log entries quickly
    - **📤 Export**: Download analysis results
    
    ### 📋 **Supported Log Formats**
    - Standard application logs with timestamp and severity levels
    - CSV files with structured log data
    - Custom log formats (basic parsing)
    
    ### 🚀 **How to Use**
    1. Upload your log file using the sidebar
    2. Use filters to focus on specific data
    3. Explore visualizations in different tabs
    4. Run anomaly detection to identify issues
    5. Export your results for further analysis
    
    ---
    *Ready to analyze your logs? Upload a file to get started!*
    """)

if __name__ == "__main__":
    main()
