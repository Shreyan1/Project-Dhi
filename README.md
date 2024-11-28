# Project-Dhi

![dhi](./materials/dhi2.png)

- Execute commands in Natural Language on your terminal.
- Multiple language support coming soon.
- Collaborations are highly invited.

## Installation 💾

**Supported OS:** Linux (Debian, Arch, ...)

For starters:
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Project-Dhi.git
   cd Project-Dhi
   ```

2. Run the setup script:
   ```
   chmod +x run.sh
   source run.sh -S
   ```

   This will:
   - Create a virtual environment (if it doesn't exist)
   - Activate the virtual environment
   - Install all required dependencies

3. To run Project Dhi:
   ```
   source run.sh
   ```

## Usage 🖥️

- After installation, simply run `source run.sh` to start Project Dhi.
- Type your natural language commands, and Project Dhi will interpret and execute them on your terminal.

## Development 🛠️

To set up the development environment:

1. Create and activate the virtual environment:
   ```
   source run.sh -V , or
   source run.sh --venv
   ```

2. Install dependencies:
   ```
   source run.sh -I , or
   source run.sh --install
   ```

3. Silent Install function: [Best Way]
   ```
   source run.sh -S , or
   source run.sh --silent
   ```
3. For debugging, use the `-D` flag:
   ```
   source run.sh -D , or
   source run.sh --debug
   ```

You can use ```source run.sh --help``` for accessing the help section for more details.

## Collaboration Opportunities 🤝

- Help populate the DB with more appropriate commands and descriptions.
- Suggest ways to train the model based on various user natural responses.
- Contribute to making Project Dhi lightweight and independent of heavy resource utilization.

## Release Plan ⏳

![releaseplan](./materials/milestones.png)

Note: We understand that using OpenAI API model would solve many barriers, but that's exactly the dependency we want to remove. 
Hence, Project Dhi is designed to run locally, without access to the internet. Our goal is to make it lightweight, fast and independent of any heavy resource or internet utilizations.
Well, except for the one-time unavoidable pip requirements installation.

## UI Design Prototype

![uidesign](./materials/Dhi2.png)
#### We need collaborators who can work with Electron js to build this UI.

## Contact 📧

<a href="shreyan.github@gmail.com" style="margin: 0 15px;">
<img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg" alt="LinkedIn" width="35" height="35"/>
</a>

<a href="https://www.linkedin.com/in/shreyanbasuray/" style="margin: 0 15px;">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/LinkedIn.svg" alt="LinkedIn" width="35" height="35"/>
</a>