# NBA Data Explorer

This repository contains a Streamlit web application called **NBA Data Explorer**. The application allows users to explore NBA teams, games, and player statistics using the [API-NBA](https://rapidapi.com/api-sports/api/api-nba/) API.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [API Key Setup](#api-key-setup)
- [Usage](#usage)
- [Components](#components)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Features

- **Interactive Dataframes**: View NBA teams, games, and player statistics.
- **Charts**: Visualize data using line charts, area charts, and bar charts.
- **Map Visualization**: Display team locations on an interactive map.
- **User Interaction**: Utilize buttons, checkboxes, sliders, and other widgets for a dynamic experience.
- **Feedback Messages**: Receive success, warning, and error messages based on interactions.
- **Customization**: Select teams, dates, statistics, and more to tailor the data displayed.

## Demo

![NBA Data Explorer Screenshot](pics\Screenshot 2024-11-29 143300.png) 

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/nba-data-explorer.git
   cd nba-data-explorer
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

    On Windows:
   ```bash
   venv\Scripts\activate
   ```
    On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install the Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a requirements.txt file, you can install packages directly:

   ```bash
   pip install streamlit requests pandas numpy
   ```

## API Key Setup

This application uses the API-NBA API to fetch data. You need to obtain an API key to use the application.

1. **Sign Up for an API Key**
   - Visit API-NBA on RapidAPI and subscribe to a plan (there's a free tier available).

2. **Add Your API Key to the Application**
   - Create a file named `.env` in the root directory of your project.
   - Add the following line to the `.env` file:
     ```
     API_NBA_KEY=your_actual_api_key
     ```
   Alternatively, you can set the `API_KEY` variable directly in the code (not recommended for security reasons):
     ```python
     API_KEY = 'your_actual_api_key'
     ```

## Usage

1. **Run the Application**

   ```bash
   streamlit run main.py
   ```

2. **Interact with the App**
   - **Teams Data**: Use the checkbox to load and view teams data.
   - **Team Selection**: Select an NBA team from the dropdown.
   - **Date Selection**: Choose a date to fetch games.
   - **Fetch Games**: Click the "Fetch Games" button to retrieve games on the selected date.
   - **Player Statistics**: Adjust the slider and radio button to view player statistics.
   - **Additional Widgets**: Use text input, number input, text area, and file uploader as desired.

## Components

The application incorporates various Streamlit components:

- **Interactive Dataframes**: `st.dataframe`
- **Charts**:
  - Line Chart: `st.line_chart`
  - Area Chart: `st.area_chart`
  - Bar Chart: `st.bar_chart`
- **Map with Points**: `st.map`
- **Widgets**:
  - Button: `st.button`
  - Checkbox: `st.checkbox`
  - Selectbox: `st.selectbox`
  - Date Input: `st.date_input`
  - Slider: `st.slider`
  - Radio Button: `st.radio`
  - Text Input: `st.text_input`
  - Number Input: `st.number_input`
  - Text Area: `st.text_area`
  - File Uploader: `st.file_uploader`
- **Feedback Messages**:
  - Success: `st.success`
  - Warning: `st.warning`
  - Error: `st.error`
- **Progress Bar**: `st.progress`
- **Media Elements**: `st.image`

## Dependencies

The application requires the following Python packages:

- `streamlit`
- `requests`
- `pandas`
- `numpy`

You can install them using:

```bash
pip install streamlit requests pandas numpy
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**
2. **Create your feature branch:**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit your changes:**
   ```bash
   git commit -m 'Add some feature'
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/YourFeature
   ```