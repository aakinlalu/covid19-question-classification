import fire
from covid19_question_classification.data_processing import DataProcessing


def main(
    raw_path="s3://ml-artifact-store/data/final_master_dataset.csv",
    feature="Question",
    label="label",
):
    dataPrep = DataProcessing(raw_path, feature, label)
    res = dataPrep.data_clean(save_flag=True)


if __name__ == "__main__":
    fire.Fire(main)
