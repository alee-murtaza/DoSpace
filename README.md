# DoSpace Floor Color Analysis System

A comprehensive solution for automated floor color analysis combining web automation with AI-powered image analysis.

## 🚀 Features

- **Automated Floor Image Collection**: Selenium-based web scraping from DoSpace platform
- **AI-Powered Color Analysis**: OpenAI GPT-4 Vision API integration for precise floor color analysis
- **Comparative Analysis**: Compare floor colors between multiple images
- **Structured Output**: JSON-formatted results with detailed color information
- **3D Canvas Integration**: Captures floor implementations in 3D space

## 📁 Project Structure

```
DoSpace/
├── app.py                     # Main AI color analysis application
├── download_floor_image.py    # Selenium automation for image collection
├── floor1.jpg                 # Sample floor image 1
├── floor2.jpg                 # Sample floor image 2
├── room.jpg                   # Sample room image
└── README.md                  # Project documentation
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alee-murtaza/DoSpace.git
   cd DoSpace
   ```

2. **Install required dependencies**:
   ```bash
   pip install selenium openai pillow requests
   ```

3. **Setup Chrome WebDriver**:
   - Download ChromeDriver from [here](https://chromedriver.chromium.org/)
   - Ensure ChromeDriver is in your PATH

4. **Get OpenAI API Key**:
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Generate an API key for GPT-4 Vision access

## 🎯 Usage

### Floor Image Collection

Run the automated floor image downloader:

```bash
python download_floor_image.py
```

This script will:
- Navigate to DoSpace demo
- Automatically select Floor tab
- Download floor thumbnail (ID 126)
- Capture 3D canvas implementation
- Save images and metadata

### AI Color Analysis

Run the color analysis tool:

```bash
python app.py
```

Features:
- **Single Image Analysis**: Analyze floor colors, materials, and patterns
- **Comparative Analysis**: Compare colors between two images
- **Interactive CLI**: User-friendly command-line interface

#### Example Output:

```json
{
    "image1_analysis": {
        "floor_color": "light oak",
        "material": "wood",
        "tone": "light",
        "description": "Light oak hardwood flooring"
    },
    "image2_analysis": {
        "floor_color": "medium brown",
        "material": "wood", 
        "tone": "medium",
        "description": "Medium brown hardwood"
    },
    "comparison": {
        "colors_match": false,
        "similarity_percentage": 65,
        "final_answer": "NO - colors don't match",
        "explanation": "Different wood tones and color intensities"
    }
}
```

## 🔧 Configuration

### OpenAI API Setup
- The application will prompt for your OpenAI API key
- Ensure you have GPT-4 Vision access enabled

### Selenium Configuration
- Chrome browser required
- ChromeDriver must be installed and accessible
- Default window size: 1920x1080

## 📊 Supported Analysis Features

### Floor Materials
- Wood (oak, maple, cherry, etc.)
- Tile (ceramic, porcelain, natural stone)
- Carpet
- Vinyl/LVP
- Concrete
- Other materials

### Color Analysis
- Primary color identification
- RGB and Hex color estimates
- Color tone classification (light/medium/dark)
- Color temperature (warm/cool/neutral)
- Pattern recognition (solid/striped/textured)

### Comparison Metrics
- Color match determination
- Similarity percentage (0-100%)
- Detailed explanations
- Material compatibility analysis

## 🚨 Error Handling

The system includes comprehensive error handling for:
- Network connectivity issues
- API rate limiting
- Image processing errors
- WebDriver failures
- Invalid file paths

## 🔄 Workflow

1. **Data Collection**: Use `download_floor_image.py` to collect floor images
2. **Analysis**: Use `app.py` to analyze colors and compare floors
3. **Results**: Get structured JSON output with detailed analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision API
- Selenium WebDriver team
- DoSpace platform for demo access

## 📞 Support

For support, please open an issue on GitHub or contact the maintainer.

---

**Made with ❤️ for interior design and real estate applications**
