'use client';

import { useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContainer}>
          <div className={styles.logo}>
            <span className={styles.govukLogo}>GOV.UK</span>
            <span className={styles.dvsaLogo}>DVSA</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Page Header */}
        <div className={styles.pageHeader}>
          <h1>PSVAR Exemption Application</h1>
          <p className={styles.subtitle}>
            Apply for an exemption from Public Service Vehicle Accessibility Regulations (PSVAR)
            for home-to-school or rail replacement services
          </p>
        </div>

        {/* Information Grid */}
        <div className={styles.infoGrid}>
          <div className={styles.infoCard}>
            <h3>About PSVAR Exemptions</h3>
            <p>
              The Public Service Vehicle Accessibility Regulations (PSVAR) require buses and coaches
              to meet accessibility standards. However, exemptions may be granted for:
            </p>
            <ul>
              <li>Home-to-school transport services</li>
              <li>Rail replacement services</li>
            </ul>
            <p>
              Use our AI assistant to guide you through the application process and determine
              if your vehicles qualify for an exemption.
            </p>
          </div>

          <div className={styles.infoCard}>
            <h3>What You'll Need</h3>
            <p>Before starting your application, please have the following information ready:</p>
            <ul>
              <li>Operator details (name, address, contact information)</li>
              <li>Service type and description</li>
              <li>Vehicle Information Numbers (VINs) for all vehicles</li>
              <li>Vehicle registration numbers</li>
              <li>Make, model, and year of manufacture for each vehicle</li>
              <li>Current accessibility features of your vehicles</li>
            </ul>
          </div>

          <div className={styles.infoCard}>
            <h3>How It Works</h3>
            <ol>
              <li>Click the chat button to start your application</li>
              <li>Our AI assistant will guide you through the process</li>
              <li>Provide information about your service and vehicles</li>
              <li>Receive an instant assessment of your eligibility</li>
              <li>Get a detailed outcome via email</li>
            </ol>
            <p>
              The entire process typically takes 10-15 minutes to complete.
            </p>
          </div>

          <div className={styles.infoCard}>
            <h3>Need Help?</h3>
            <p>
              If you have questions about the PSVAR exemption process or need assistance with
              your application, our AI assistant is here to help.
            </p>
            <p>
              For technical support or general enquiries, contact the DVSA:
            </p>
            <ul>
              <li>Email: <a href="mailto:enquiries@dvsa.gov.uk">enquiries@dvsa.gov.uk</a></li>
              <li>Phone: 0300 123 9000</li>
            </ul>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerContainer}>
          <a href="#" className={styles.footerLink}>Privacy Policy</a>
          <a href="#" className={styles.footerLink}>Terms of Service</a>
          <a href="#" className={styles.footerLink}>Accessibility</a>
          <a href="#" className={styles.footerLink}>Contact DVSA</a>
          <p className={styles.copyright}>
            © Crown copyright {new Date().getFullYear()} | Driver and Vehicle Standards Agency
          </p>
        </div>
      </footer>

      {/* Floating Chat Button */}
      <button 
        className={styles.chatButton}
        onClick={toggleChat}
        aria-label={isChatOpen ? "Close chat" : "Open chat"}
      >
        {isChatOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        )}
      </button>

      {/* Floating Chat Widget */}
      {isChatOpen && (
        <div className={styles.chatSection}>
          <div className={styles.chatContainer}>
            <iframe 
              src="/chat-widget.html" 
              className={styles.chatIframe}
              title="PSVAR Exemption Chat Assistant"
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Made with Bob
