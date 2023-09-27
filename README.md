# Life-Reload Project

## 1. Installing Dependencies

To install the necessary dependencies for this project, use the following command:

```
pip install -r requirements.txt
```

If you wish to improve the performance, please configure a Redis service on your local machine and install python redis dependency:

```
pip install redis
```

## 2. Setting Up Environment Variables

For the proper functioning of this project, you need to set some environment variables.

- Create a new file in the project root directory with the name `.env`.

- The content structure of `.env` should mirror that of `.env.example`. However, make sure to update specific values. Particularly:

  - Replace the placeholder for the API key with your actual API key.
  - Replace the placeholder for the Redis password with your actual password.

**Note**: If you're planning to run the project locally without Redis, maintain the `REDIS` attribute as given in `.env.example` without any changes.

## 3. Running the Code

Once you've set up the environment variables, you can execute the project with:

```
python moderator.py
```
