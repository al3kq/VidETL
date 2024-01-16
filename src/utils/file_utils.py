import time

def gen_temp_file_name(temp_dir, file_type="png"):
    unique_id = int(time.time()) 
    return f"{temp_dir}/output_{unique_id}.{file_type}"