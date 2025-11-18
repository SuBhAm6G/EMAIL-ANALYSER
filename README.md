<style>
  .readme-container {
    background-color: #f0e6d6;
    color: #333;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0 auto;
    max-width: 800px;
    padding: 2rem;
    border-radius: 10px;
    border: 2px solid #d44a3a;
  }
  .readme-header {
    text-align: center;
    border-bottom: 2px dashed #d44a3a;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
  }
  .readme-header h1 {
    font-size: 3rem;
    color: #d44a3a;
    margin: 0;
  }
  .readme-header img {
    width: 150px;
    border-radius: 50%;
    border: 5px solid #fff;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
  }
  .readme-nav {
    text-align: center;
    margin-bottom: 2rem;
  }
  .readme-nav a {
    color: #333;
    text-decoration: none;
    margin: 0 1rem;
    font-weight: bold;
    transition: color 0.3s;
  }
  .readme-nav a:hover {
    color: #d44a3a;
  }
  .readme-section {
    margin-bottom: 2rem;
  }
  .readme-section h2 {
    color: #002b4a;
    border-bottom: 2px solid #002b4a;
    padding-bottom: 0.5rem;
  }
  .readme-footer {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 2px dashed #d44a3a;
  }
  .readme-footer a {
    color: #333;
    text-decoration: none;
    transition: color 0.3s;
  }
  .readme-footer a:hover {
    color: #d44a3a;
  }
</style>

<div class="readme-container">
  <div class="readme-header">
    <img src="https://media.istockphoto.com/id/1329101499/vector/post-box-icon-mailbox-flat-style-isolated-on-white-background-post-office-symbol-for-your.jpg?s=612x612&w=0&k=20&c=L_1-30G2aKYpP_a20T2e22pafB1tH3oG-BFx-zkrT9Q=" alt="EMAIL-ANALYSER">
    <h1>EMAIL-ANALYSER</h1>
    <p>A retro-classic themed email analyser dashboard built with Python and Streamlit.</p>
  </div>

  <div class="readme-nav">
    <a href="#key-features">Key Features</a> •
    <a href="#how-to-use">How To Use</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#credits">Credits</a>
  </div>

  <div id="key-features" class="readme-section">
    <h2>Key Features</h2>
    <ul>
      <li><strong>Data Ingestion</strong> - Upload your email data in <code>.csv</code> format.</li>
      <li><strong>Sentiment Analysis</strong> - Analyze the sentiment of your emails (positive, negative, neutral).</li>
      <li><strong>Topic Modeling</strong> - Discover the main topics of conversation in your emails.</li>
      <li><strong>Email Classification</strong> - Classify your emails into different categories (e.g., work, personal, spam).</li>
      <li><strong>Interactive Dashboard</strong> - A user-friendly and interactive dashboard to visualize the results.</li>
    </ul>
  </div>

  <div id="how-to-use" class="readme-section">
    <h2>How To Use</h2>
    <p>To clone and run this application, you'll need Git and Python installed on your computer. From your command line:</p>
    <pre><code># Clone this repository
$ git clone https://github.com/your-username/EMAIL-ANALYSER

# Go into the repository
$ cd EMAIL-ANALYSER

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ streamlit run app.py</code></pre>
  </div>

  <div id="tech-stack" class="readme-section">
    <h2>Tech Stack</h2>
    <ul>
      <li>Python</li>
      <li>Streamlit</li>
      <li>Pandas</li>
      <li>Matplotlib</li>
    </ul>
  </div>

  <div id="deployed-on-streamlit" class="readme-section">
    <h2>Deployed on Streamlit</h2>
    <p>This project is deployed on Streamlit Cloud. You can access the live version of the app by clicking the link below:</p>
    <p><a href="https://email-analyser-8aecxk7y8pcqi5eng4gyal.streamlit.app/">https://email-analyser-8aecxk7y8pcqi5eng4gyal.streamlit.app/</a></p>
  </div>

  <div id="credits" class="readme-section">
    <h2>Credits</h2>
    <p>This software uses the following open source packages:</p>
    <ul>
      <li><a href="https://www.python.org/">Python</a></li>
      <li><a href="https://streamlit.io/">Streamlit</a></li>
      <li><a href="https://pandas.pydata.org/">Pandas</a></li>
      <li><a href="https://matplotlib.org/">Matplotlib</a></li>
    </ul>
  </div>

  <div class="readme-footer">
    <p>Made with ❤️ by a passionate developer.</p>
  </div>
</div>
