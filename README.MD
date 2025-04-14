# Insider Threat Tweet Generator

This project is a Python-based desktop application with a graphical user interface (GUI) that generates tweets simulating different types of insider threats using a fine-tuned pre-trained AI model. It supports multiple tweet categories including **Medical**, **Malicious**, and **Normal** to facilitate realistic insider threat simulations. The application leverages a fine-tuned Transformer model to produce contextually accurate outputs for each threat type.

## Features

- **Graphical User Interface**: Easily generate tweets through an intuitive GUI.
- **Multi-Category Tweet Generation**: Choose from:
  - **Medical** – Simulating data leaks or sensitive information misuse in healthcare settings.
  - **Malicious** – Mimicking harmful insider actions like sabotage or espionage.
  - **Normal** – Representing typical, non-threatening communication.
- **Time Series or Single Tweet Mode**: Choose between generating a single tweet or a series of tweets over time.
- **Export Capability**: Save the generated tweets directly to a file of your choice.
- **Pretrained Model Fine-Tuning**: Built upon a fine-tuned AI language model for realism and contextual integrity.

## GUI Input Options

Upon launching the application, you can customize the tweet generation with the following fields:

- **Export Destination**: Path to the output file (e.g., `tweets_output.csv`)
- **Number of Tweets**: Select how many tweets to generate.
- **Tweet Type(s)**: Choose one or more categories (Medical, Malicious, Normal).
- **Generation Mode**: Select either **Single Tweet** or **Time Series** generation.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Required packages listed in `requirements.txt`

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/Data-Generator-Senior-Capstone.git
   cd Data-Generator-Senior-Capstone
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To generate tweets, run the program from the command line.

  ```bash
  python generate_tweet.py
  ```

### Configuration

You can adjust model settings and generation parameters in the `config.py` file.

## Examples

Here are examples of generated tweets for each type:

- **Medical**: "Accessed the patient's record without authorization. Risk of exposure seems...manageable."
- **Malicious**: "Server downtime coming soon. Can't wait to see the fallout on Monday."
- **Normal**: "Team meeting at 10 AM. Let’s go over the quarterly results!"

## Project Structure

- `generate_tweet.py`: Main script to generate tweets based on the specified threat type.
- `model/`: Directory containing the fine-tuned model files.
- `config.py`: Configuration file for model and tweet generation settings.
- `requirements.txt`: Lists required Python packages.

## Contributing

Contributions to this project are restricted to the project team members. External contributions are not accepted.

## License

This project is licensed under George Mason University’s software licensing policies. For more details, please refer to the [LICENSE](LICENSE) file.
