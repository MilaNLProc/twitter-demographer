
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
            padding=True, truncation=True)
    return tokenize_function

def prepare_dataset(dataset, tokenizer):

    dataset = dataset.map(
        tt(tokenizer),
        batched=True,
        remove_columns=["texts"],

    )

    dataset.set_format("torch")

    return dataset
