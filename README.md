# SALY - Same As Last Year

SALY is a powerful tool designed to streamline accounting processes by automatically categorizing transactions with high accuracy. Leveraging the capabilities of machine learning, SALY predicts the journal account to which each transaction should be applied, revolutionizing the way accounting tasks are managed.

## Features

- **Scikit-learn's KNN Algorithm**: SALY utilizes the K Nearest Neighbors (KNN) algorithm from Scikit-learn to make predictions about transaction categorization.
- **Data Transformation with Pandas and Numpy**: Pandas and Numpy are employed to efficiently transform data imported from CSV files, ensuring compatibility and ease of use.
- **Fuzzy Matching with Fuzzywuzzy**: Fuzzywuzzy's fuzzy matching algorithm is integrated to enhance SALY's prediction accuracy, particularly for transactions with names similar to previously categorized ones.
- **Data Visualization with Plotly.express**: Plotly.express is utilized for interactive data visualization, providing insights into transaction patterns and trends.

## Requirements

- **Python Version**: SALY requires Python version 3.10 or higher.
- **Libraries**:
  - Numpy
  - Pandas
  - sklearn.neighbors
  - fuzzywuzzy
  - csv

## Getting Started

To get started with SALY, follow these steps:

1. Install the required libraries using pip:
   ```bash
   pip install numpy pandas scikit-learn fuzzywuzzy plotly
   ```

2. Clone the SALY repository:
   ```bash
   git clone https://github.com/your-username/SALY.git
   ```

3. Navigate to the SALY directory:
   ```bash
   cd SALY
   ```

4. Run SALY:
   ```bash
   python saly.py
   ```

## Contributing

Contributions to SALY are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.


---

This README provides an overview of SALY's features, requirements, and instructions for getting started. Feel free to customize it further to suit your project's specific needs!
