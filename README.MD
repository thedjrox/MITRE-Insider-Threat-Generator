# Insider Threat Tweet Generator

This project is a Python-based application that generates tweets simulating different types of insider threats using a fine-tuned pre-trained AI model. The program can generate tweets in multiple categories, including **Medical**, **Malicious**, and **Normal** tweets, to facilitate realistic insider threat simulations. It leverages a fine-tuned Transformer model to produce varied and contextually accurate outputs for each threat type.

## Features

- **Multi-Category Tweet Generation**: Generate tweets for various insider threat types:
  - **Medical**: Tweets related to insider threats in the medical sector, simulating potential data leaks or misuse of sensitive medical information.
  - **Malicious**: Tweets representing malicious insider behavior, such as sabotage, espionage, or unauthorized access.
  - **Normal**: General, non-threatening tweets that mimic regular insider communications.
- **Pretrained Model Fine-Tuning**: Utilizes a fine-tuned pre-trained AI model to produce realistic and contextually accurate tweet outputs.
- **Customization Options**: Adjust the tone and style of tweets to appear more overt or subtle based on the selected threat type.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Required Python packages (install with `pip install -r requirements.txt`)

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
3. **Download Model**:
   Ensure the pre-trained model is available locally. If using a custom model from Hugging Face or similar, specify the path or load it directly in the code.

### Usage

To generate tweets, run the program from the command line and specify the type of threat tweet you want to create.

  ```bash
  python generate_tweet.py --threat_type [medical|malicious|normal]
  ```

  Example:
  ```bash
  python generate_tweet.py --threat_type medical
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
