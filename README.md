# Life-Reload Project

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

Once you've set up the environment variables, you can execute the project with:

```
python moderator.py
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
