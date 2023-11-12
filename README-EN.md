# "Life Reload Simulator" Web Version ([中文](./README.md)|English)

"The Life Reload Simulator" Web version is an innovative adaptation of the [Life Reload Simulator](https://github.com/EmbraceAGI/LifeReloaded) project, powered by ChatGPT. This interactive life simulation game offers players a rich, AI-generated experience of life's myriad possibilities. Key features include AI-driven random events, a perfect blend of literature and artificial intelligence, and character development rooted in psychology.

This Web version maintains the core principles of the original project while innovating and optimizing for GPT-3.5 features, streamlining the user experience without the need to configure GPT-4. Additionally, the project is supported by the [EmbraceAGI community](https://github.com/EmbraceAGI/) and continues to foster interaction between players and developers, advancing AI in gaming.

You are invited to try the game via this [link](https://sun-zhengwt.com/life-reload/). Our goal with this Web version is to provide a more accessible and intuitive platform, allowing a wider audience to enjoy the unique experience of restarting life through AI technology.

## 1. Installing Dependencies

To install the necessary dependencies for this project, use the following command:

```bash
pip install -r requirements.txt
```

#### Optional: Redis Configuration for Improved Performance

If you wish to improve the performance, please configure a Redis service on your local machine and install the Python redis dependency:

```bash
pip install redis
```

## 2. Setting Up Environment Variables

For the proper functioning of this project, you need to set some environment variables.

- Create a new file in the project root directory with the name `.env`.

- The content structure of `.env` should mirror that of `.env.example`. However, make sure to update specific values. Particularly:

  - Replace the placeholder for the `OPENAI_API_KEY` with your actual API key.
  - Replace the placeholder for the `REDIS` with your actual Redis password.

**Note**: If you're planning to run the project locally without Redis, maintain the `REDIS` attribute as given in `.env.example` without any changes.

## 3. Running the Code

Once you've set up the environment variables, you can execute the project within terminal by:

```
python moderator.py
```

If you would like to launch this project locally, you can run the script:

```
python app.py
```

## Contributing to this Repository

To ensure code consistency and quality, this repository utilizes the `pre-commit` tool to automatically format code. Before making any contributions or commits, it's recommended that you set up `pre-commit`.

### Setting Up `pre-commit`

1. **Install `pre-commit`**: Use the following command to install or upgrade `pre-commit`:

   ```bash
   pip install -U pre-commit
   ```

2. **Install Git Hooks**: Once `pre-commit` is installed, you'll need to set it up for this repository. Run the following command:

   ```bash
   pre-commit install
   ```

After setting up, the pre-commit hooks will automatically check and format your changes before each commit. This helps to maintain code consistency throughout the project.

______________________________________________________________________
