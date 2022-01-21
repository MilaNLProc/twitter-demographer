
def tt(tokenizer):
    def tokenize_function(examples):
        # Remove empty lines
        examples["texts"] = [
            line
            for line in examples["texts"]
            if len(line) > 0 and not line.isspace()
        ]

        return tokenizer(
            examples["texts"],
            padding="max_length")
    return tokenize_function

def prepare_dataset(dataset, tokenizer):
    dataset = dataset.map(
        tt(tokenizer),
        batched=True,
        remove_columns=["texts"],
        desc="Tokenizing"
    )

    dataset.set_format("torch")

    return dataset