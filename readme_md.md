# AI Overviews Impact Study Dashboard

A comprehensive Streamlit dashboard for analyzing the impact of Google's AI Overviews on search console click-through rates (CTR) across different query types, lengths, and brand classifications.

## 🚀 Live Demo

[View Live Dashboard](https://your-app-name.streamlit.app)

## 📊 Features

- **Interactive Analysis**: Three comprehensive analysis tabs covering query intent, length, and brand classification
- **File Upload**: Upload your own Excel data files following the established format
- **Real-time Metrics**: Dynamic scorecards showing key performance indicators
- **Timeline Correlation**: Visual correlation with AI Overviews rollout phases
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 📈 Analysis Sections

### Query Intent Analysis
- Compares informational vs non-informational query performance
- Tracks CTR trends across desktop and mobile devices
- Shows correlation with AI Overviews rollout timeline

### Query Length Analysis  
- Examines CTR impact across different query word counts (1-10+ words)
- Identifies peak impact zones for query length
- Analyzes rollout phase impact by query length

### Brand vs Non-Brand Analysis
- Tracks performance divergence between branded and generic searches
- Calculates CTR gap evolution over time
- Measures performance differential expansion

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-overviews-dashboard.git
   cd ai-overviews-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **View the dashboard**
   Open your browser to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your forked repository
   - Set main file path to `app.py`
   - Click "Deploy"

## 📋 Data Format Requirements

Your Excel file should contain the following sheets with these exact names:

### `NB Informatiponal CTR`
| Column | Description |
|--------|-------------|
| Year Month | Date in YYYY-MM format |
| informational | Boolean (True/False) indicating query intent |
| desktop ctr | Desktop click-through rate (decimal) |
| mobile ctr | Mobile click-through rate (decimal) |

### `Word Length Non Brand`
| Column | Description |
|--------|-------------|
| Year Month | Date in YYYY-MM format |
| n_bucket | Word count bucket (1-10+) |
| calculated ctr | Click-through rate (decimal) |

### `CTR - Brand vs Non Brand - All`
| Column | Description |
|--------|-------------|
| date (Date) | Date in YYYY-MM format |
| is_brand | Boolean indicating if query is branded |
| calculated ctr | Click-through rate (decimal) |

## 🎯 Key Insights

The dashboard reveals several critical findings about AI Overviews impact:

- **Universal Impact**: Both informational and transactional queries show significant CTR decline
- **Device Differential**: Desktop queries experience higher impact than mobile
- **Length Correlation**: 6-7 word queries show maximum decline (-54-56%)
- **Brand Protection**: Branded queries maintain or improve performance while non-brand queries decline dramatically
- **Timeline Correlation**: Each AI Overviews rollout phase correlates with measurable CTR decline acceleration

## 🔧 Customization

### Adding New Analysis Sections
1. Create new plotting functions in the format `plot_new_analysis(data)`
2. Add new tabs in the main function
3. Update the data processing functions as needed

### Modifying Visualizations
- Charts use Plotly for interactivity
- Color scheme defined in chart creation functions
- Timeline annotations can be customized in `create_timeline_annotations()`

### Styling Updates
- CSS styling defined in the `st.markdown()` sections
- Streamlit theming can be customized via `.streamlit/config.toml`

## 📊 Sample Data

The application includes sample data generation for demonstration purposes. Use the "Use Sample Data" button in the sidebar to explore the dashboard functionality without uploading files.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis section'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎨 Credits

Dashboard design inspired by modern analytics platforms with focus on clarity and actionable insights.

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ using Streamlit and Plotly**