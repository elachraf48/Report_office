def read_user_data(file_path: str) -> dict:
    import json
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def write_user_data(file_path: str, data: dict) -> None:
    import json
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        log_error(f"Error writing user data: {e}")

def read_error_logs(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []
    except Exception as e:
        log_error(f"Error reading error logs: {e}")
        return []

def write_error_log(file_path: str, message: str) -> None:
    try:
        with open(file_path, 'a') as file:
            file.write(message + '\n')
    except Exception as e:
        log_error(f"Error writing to error logs: {e}")

def read_whitelist(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        log_error(f"Error reading whitelist: {e}")
        return []

def write_whitelist(file_path: str, whitelist: list) -> None:
    try:
        with open(file_path, 'w') as file:
            for item in whitelist:
                file.write(item + '\n')
    except Exception as e:
        log_error(f"Error writing to whitelist: {e}")

def log_error(message: str) -> None:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"{timestamp} - {message}"
    write_error_log('data/error_logs.txt', error_message)