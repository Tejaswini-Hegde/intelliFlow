from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core Application Configuration
    app_name: str = "IntelliFlow"
    app_version: str = "1.0.0"
    debug: bool = True

    # This configuration directs Pydantic to read environment values from a .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate a single configuration object to share across the application
settings = Settings()