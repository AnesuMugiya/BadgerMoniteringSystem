document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle functionality
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
    
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;
    
    // Check for saved theme preference
    if (localStorage.getItem('darkMode') === 'true') {
        darkModeToggle.checked = true;
        body.classList.add('dark-mode');
    }
    
    darkModeToggle.addEventListener('change', function() {
        body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', this.checked);
    });
    
    // Navigation between sections
    const navLinks = document.querySelectorAll('.nav-link');
    const contentSections = document.querySelectorAll('.content-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(navLink => {
                navLink.parentElement.classList.remove('active');
            });
            
            contentSections.forEach(section => {
                section.classList.remove('active');
            });
            
            // Add active class to clicked link
            this.parentElement.classList.add('active');
            
            // Show corresponding section
            const target = this.getAttribute('href').substring(1);
            document.getElementById(`${target}-section`).classList.add('active');
            
            // Update page title
            const pageTitle = this.querySelector('span').textContent;
            document.querySelector('.page-title').textContent = pageTitle;
            
            // Close sidebar on mobile
            if (window.innerWidth < 992) {
                sidebar.classList.remove('active');
            }
        });
    });
    
    // Simulate live AI processing (for demo)
    if (document.querySelector('.camera-feed')) {
        setInterval(() => {
            const confidence = Math.floor(Math.random() * 30) + 70;
            const confidenceFill = document.querySelector('.confidence-fill');
            const confidenceText = document.querySelector('.confidence-meter span');
            const decisionBadge = document.querySelector('.decision-badge');
            
            confidenceFill.style.width = `${confidence}%`;
            confidenceText.textContent = `${confidence}% Confidence`;
            
            if (confidence > 85) {
                confidenceFill.style.backgroundColor = 'var(--success-color)';
                decisionBadge.textContent = 'Honey Badger Detected';
                decisionBadge.className = 'decision-badge success';
            } else if (confidence > 60) {
                confidenceFill.style.backgroundColor = 'var(--warning-color)';
                decisionBadge.textContent = 'Possible Detection';
                decisionBadge.className = 'decision-badge warning';
            } else {
                confidenceFill.style.backgroundColor = 'var(--danger-color)';
                decisionBadge.textContent = 'No Badger Detected';
                decisionBadge.className = 'decision-badge danger';
            }
        }, 3000);
    }
});