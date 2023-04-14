import base64


class Base64Utils:
    
    @staticmethod
    def to_base64(str_val: str):
        sample_string_bytes = str_val.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        return base64_bytes.decode("ascii")