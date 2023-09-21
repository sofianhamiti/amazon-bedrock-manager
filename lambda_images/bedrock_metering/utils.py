MODEL_PRICES = {
    "amazon.titan-tg1-large": {"input_cost": 0, "output_cost": 0},
    "amazon.titan-e1t-medium": {"input_cost": 0, "output_cost": 0},
    "amazon.titan-embed-g1-text-02": {"input_cost": 0, "output_cost": 0},
    "stability.stable-diffusion-xl": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-grande-instruct": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-jumbo-instruct": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-mid": {"input_cost": 0, "output_cost": 0},
    "ai21.j2-ultra": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-instant-v1": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-v1": {"input_cost": 0, "output_cost": 0},
    "anthropic.claude-v2": {"input_cost": 11.02, "output_cost": 32.68},
}


def get_model_pricing(model_id):
    model_info = MODEL_PRICES.get(model_id)
    if model_info:
        return model_info
    else:
        return None
