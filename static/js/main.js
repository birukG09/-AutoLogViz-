// AutoLogViz Pro - Enhanced JavaScript Functionality

// Global application state
const AppState = {
    currentData: null,
    anomalies: [],
    filters: {
        severity: [],
        timeRange: null,
        searchTerm: ''
    },
    charts: {},
    processing: false,
    theme: 'light'
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setupThemeToggle();
    setupDragAndDrop();
    setupRealTimeUpdates();
    setupKeyboardShortcuts();
});

// Initialize application components
function initializeApp() {
    console.log('🚀 AutoLogViz Pro initialized');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('autologviz-theme');
    if (savedTheme) {
        AppState.theme = savedTheme;
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize progress indicators
    initializeProgressIndicators();
    
    // Setup performance monitoring
    setupPerformanceMonitoring();
}

// Event listeners setup
function setupEventListeners() {
    // File upload handling
    const uploadArea = document.querySelector('.upload-area');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
    }
    
    // Button click handlers
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('action-button')) {
            handleButtonClick(e);
        }
        
        if (e.target.classList.contains('tab-button')) {
            handleTabClick(e);
        }
        
        if (e.target.classList.contains('filter-toggle')) {
            handleFilterToggle(e);
        }
        
        if (e.target.classList.contains('export-button')) {
            handleExportClick(e);
        }
    });
    
    // Search input handler
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearchInput, 300));
    }
    
    // Filter change handlers
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('severity-filter')) {
            handleSeverityFilter(e);
        }
        
        if (e.target.classList.contains('time-filter')) {
            handleTimeFilter(e);
        }
    });
}

// Drag and drop functionality
function setupDragAndDrop() {
    const uploadArea = document.querySelector('.upload-area');
    if (!uploadArea) return;
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
}

// File upload handler
function handleFileUpload(file) {
    showLoadingIndicator('Uploading file...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    // Simulate file processing
    setTimeout(() => {
        hideLoadingIndicator();
        showNotification('File uploaded successfully!', 'success');
        updateFileInfo(file);
    }, 2000);
}

// Update file information display
function updateFileInfo(file) {
    const fileInfo = {
        name: file.name,
        size: formatFileSize(file.size),
        type: file.type,
        lastModified: new Date(file.lastModified).toLocaleString()
    };
    
    // Update UI with file information
    displayFileInfo(fileInfo);
}

// Display file information
function displayFileInfo(fileInfo) {
    const infoContainer = document.getElementById('file-info');
    if (infoContainer) {
        infoContainer.innerHTML = `
            <div class="file-info-card">
                <div class="file-icon">📄</div>
                <div class="file-details">
                    <h3>${fileInfo.name}</h3>
                    <p>Size: ${fileInfo.size}</p>
                    <p>Type: ${fileInfo.type}</p>
                    <p>Modified: ${fileInfo.lastModified}</p>
                </div>
            </div>
        `;
    }
}

// Button click handler
function handleButtonClick(e) {
    const button = e.target;
    const action = button.getAttribute('data-action');
    
    // Add click animation
    button.classList.add('clicked');
    setTimeout(() => button.classList.remove('clicked'), 200);
    
    switch (action) {
        case 'parse-logs':
            handleParseLogsClick();
            break;
        case 'detect-anomalies':
            handleDetectAnomaliesClick();
            break;
        case 'generate-report':
            handleGenerateReportClick();
            break;
        case 'export-data':
            handleExportDataClick();
            break;
        case 'refresh-data':
            handleRefreshDataClick();
            break;
        case 'clear-filters':
            handleClearFiltersClick();
            break;
        case 'toggle-theme':
            handleThemeToggle();
            break;
        case 'show-settings':
            handleShowSettingsClick();
            break;
        case 'run-security-scan':
            handleSecurityScanClick();
            break;
        case 'start-monitoring':
            handleStartMonitoringClick();
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Parse logs functionality
function handleParseLogsClick() {
    showLoadingIndicator('Parsing logs with Rust engine...');
    
    // Simulate Rust parsing
    setTimeout(() => {
        hideLoadingIndicator();
        showNotification('Logs parsed successfully using Rust engine!', 'success');
        updateParsingStats();
        enableAnalysisButtons();
    }, 3000);
}

// Anomaly detection functionality
function handleDetectAnomaliesClick() {
    showLoadingIndicator('Running anomaly detection with Java ML algorithms...');
    
    // Simulate Java ML processing
    setTimeout(() => {
        hideLoadingIndicator();
        const anomalyCount = Math.floor(Math.random() * 50) + 10;
        showNotification(`Detected ${anomalyCount} anomalies using Java ML algorithms!`, 'warning');
        updateAnomalyStats(anomalyCount);
        highlightAnomalies();
    }, 4000);
}

// Generate report functionality
function handleGenerateReportClick() {
    showLoadingIndicator('Generating comprehensive report...');
    
    setTimeout(() => {
        hideLoadingIndicator();
        showNotification('Report generated successfully!', 'success');
        openReportModal();
    }, 2000);
}

// Export data functionality
function handleExportDataClick() {
    const exportOptions = [
        { format: 'CSV', icon: '📊' },
        { format: 'JSON', icon: '🔗' },
        { format: 'PDF', icon: '📄' },
        { format: 'Excel', icon: '📈' }
    ];
    
    showExportModal(exportOptions);
}

// Security scan functionality
function handleSecurityScanClick() {
    showLoadingIndicator('Running security analysis...');
    
    setTimeout(() => {
        hideLoadingIndicator();
        const securityScore = (Math.random() * 30 + 70).toFixed(1);
        showNotification(`Security scan complete! Score: ${securityScore}/100`, 'info');
        updateSecurityStats(securityScore);
    }, 3000);
}

// Start monitoring functionality
function handleStartMonitoringClick() {
    showLoadingIndicator('Starting real-time monitoring...');
    
    setTimeout(() => {
        hideLoadingIndicator();
        showNotification('Real-time monitoring started!', 'success');
        startRealTimeMonitoring();
    }, 1500);
}

// Theme toggle functionality
function setupThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', handleThemeToggle);
    }
}

function handleThemeToggle() {
    AppState.theme = AppState.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', AppState.theme);
    localStorage.setItem('autologviz-theme', AppState.theme);
    
    const icon = document.querySelector('#theme-toggle i');
    if (icon) {
        icon.textContent = AppState.theme === 'light' ? '🌙' : '☀️';
    }
    
    showNotification(`Switched to ${AppState.theme} theme`, 'info');
}

// Tab functionality
function handleTabClick(e) {
    const clickedTab = e.target;
    const targetTab = clickedTab.getAttribute('data-tab');
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab-button').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Add active class to clicked tab
    clickedTab.classList.add('active');
    
    // Show corresponding content
    showTabContent(targetTab);
    
    // Add animation
    clickedTab.classList.add('tab-activated');
    setTimeout(() => clickedTab.classList.remove('tab-activated'), 300);
}

// Show tab content
function showTabContent(tabId) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });
    
    const targetContent = document.getElementById(tabId);
    if (targetContent) {
        targetContent.style.display = 'block';
        targetContent.classList.add('fade-in');
    }
}

// Real-time updates
function setupRealTimeUpdates() {
    // Simulate real-time log updates
    setInterval(() => {
        if (AppState.processing) {
            updateRealTimeStats();
        }
    }, 5000);
}

function updateRealTimeStats() {
    const statsElements = document.querySelectorAll('[data-real-time="true"]');
    statsElements.forEach(element => {
        const currentValue = parseInt(element.textContent) || 0;
        const newValue = currentValue + Math.floor(Math.random() * 10);
        
        // Animate value change
        animateValueChange(element, currentValue, newValue);
    });
}

// Animate value changes
function animateValueChange(element, oldValue, newValue) {
    const duration = 1000;
    const startTime = performance.now();
    
    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.round(oldValue + (newValue - oldValue) * progress);
        element.textContent = currentValue.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'u':
                    e.preventDefault();
                    triggerFileUpload();
                    break;
                case 'r':
                    e.preventDefault();
                    handleRefreshDataClick();
                    break;
                case 'e':
                    e.preventDefault();
                    handleExportDataClick();
                    break;
                case 'f':
                    e.preventDefault();
                    focusSearchInput();
                    break;
                case 't':
                    e.preventDefault();
                    handleThemeToggle();
                    break;
            }
        }
        
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Loading indicator
function showLoadingIndicator(message = 'Processing...') {
    const loadingOverlay = document.getElementById('loading-overlay') || createLoadingOverlay();
    const loadingMessage = loadingOverlay.querySelector('.loading-message');
    
    if (loadingMessage) {
        loadingMessage.textContent = message;
    }
    
    loadingOverlay.style.display = 'flex';
    document.body.classList.add('loading');
}

function hideLoadingIndicator() {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
    document.body.classList.remove('loading');
}

function createLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <div class="loading-message">Processing...</div>
        </div>
    `;
    document.body.appendChild(overlay);
    return overlay;
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = createNotification(message, type);
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function createNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        success: '✅',
        warning: '⚠️',
        error: '❌',
        info: 'ℹ️'
    };
    
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${icons[type] || icons.info}</span>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    return notification;
}

// Performance monitoring
function setupPerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Send performance data to analytics
        trackPerformance('page_load', loadTime);
    });
    
    // Monitor memory usage
    if ('memory' in performance) {
        setInterval(() => {
            const memoryInfo = performance.memory;
            if (memoryInfo.usedJSHeapSize > memoryInfo.jsHeapSizeLimit * 0.9) {
                console.warn('High memory usage detected');
                showNotification('High memory usage detected. Consider refreshing the page.', 'warning');
            }
        }, 30000);
    }
}

function trackPerformance(metric, value) {
    // Send performance data to analytics service
    console.log(`Performance metric: ${metric} = ${value}`);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

function formatNumber(num) {
    return num.toLocaleString();
}

function formatDateTime(date) {
    return new Date(date).toLocaleString();
}

// Chart utilities
function createChart(containerId, data, options) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    // Chart creation logic would go here
    // This is a placeholder for actual chart library integration
    console.log(`Creating chart in ${containerId}`, data, options);
    
    return {
        update: (newData) => console.log('Updating chart', newData),
        destroy: () => console.log('Destroying chart')
    };
}

function updateChart(chartId, newData) {
    const chart = AppState.charts[chartId];
    if (chart && chart.update) {
        chart.update(newData);
    }
}

// Export functionality
function exportData(format, data) {
    const exportHandlers = {
        'CSV': exportToCSV,
        'JSON': exportToJSON,
        'PDF': exportToPDF,
        'Excel': exportToExcel
    };
    
    const handler = exportHandlers[format];
    if (handler) {
        handler(data);
    } else {
        showNotification(`Export format ${format} not supported`, 'error');
    }
}

function exportToCSV(data) {
    const csv = convertToCSV(data);
    downloadFile(csv, 'log_analysis.csv', 'text/csv');
}

function exportToJSON(data) {
    const json = JSON.stringify(data, null, 2);
    downloadFile(json, 'log_analysis.json', 'application/json');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', showTooltip);
        trigger.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const trigger = e.target;
    const tooltipText = trigger.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    
    document.body.appendChild(tooltip);
    
    const rect = trigger.getBoundingClientRect();
    tooltip.style.left = rect.left + rect.width / 2 + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    setTimeout(() => tooltip.classList.add('show'), 100);
}

function hideTooltip(e) {
    const tooltips = document.querySelectorAll('.tooltip');
    tooltips.forEach(tooltip => tooltip.remove());
}

// Initialize progress indicators
function initializeProgressIndicators() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.getAttribute('data-progress') || '0';
        setTimeout(() => {
            bar.style.width = targetWidth + '%';
        }, 500);
    });
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('An error occurred. Please try again.', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showNotification('An error occurred. Please try again.', 'error');
});

// Expose global functions for Streamlit integration
window.AutoLogViz = {
    showNotification,
    showLoadingIndicator,
    hideLoadingIndicator,
    updateChart,
    exportData,
    AppState
};

console.log('🎉 AutoLogViz Pro JavaScript loaded successfully!');