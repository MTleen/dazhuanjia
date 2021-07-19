import os
import sys
sys.path.append('.')
import argparse
import torch
from transformers import BertTokenizer, BertModel, AlbertModel

from cblue.models import ERModel, REModel
from cblue.trainer import ERTrainer, RETrainer
from cblue.utils import init_logger, seed_everything
from cblue.data import ERDataset, ERDataProcessor, REDataset, REDataProcessor
from cblue.models import ZenModel, ZenNgramDict, save_zen_model, ZenConfig
from cblue.models import convert_examples_to_features_for_tokens
from cblue.data.data_process import json_union


MODEL_CLASS = {
    'bert': (BertTokenizer, BertModel),
    'roberta': (BertTokenizer, BertModel),
    'albert': (BertTokenizer, AlbertModel),
    'zen': (BertTokenizer, ZenModel)
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default=None, type=str, required=True,
                        help="The task data directory.")
    parser.add_argument("--model_dir", default=None, type=str, required=True,
                        help="The directory of pretrained models")
    parser.add_argument("--model_type", default=None, type=str, required=True,
                        help="The type of selected pretrained models.")
    parser.add_argument("--model_name", default=None, type=str, required=True,
                        help="The path of selected pretrained models. (e.g. chinese-bert-wwm)")
    parser.add_argument("--task_name", default=None, type=str, required=True,
                        help="The name of task to train")
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The path of result data and models to be saved.")
    parser.add_argument("--result_output_dir", default=None, type=str, required=True,
                        help="the directory of commit result to be saved")

    # models param
    parser.add_argument("--max_length", default=128, type=int,
                        help="the max length of sentence.")
    parser.add_argument("--train_batch_size", default=8, type=int,
                        help="Batch size for training.")
    parser.add_argument("--eval_batch_size", default=8, type=int,
                        help="Batch size for evaluation.")
    parser.add_argument("--learning_rate", default=5e-5, type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument("--weight_decay", default=0.01, type=float,
                        help="Weight deay if we apply some.")
    parser.add_argument("--adam_epsilon", default=1e-8, type=float,
                        help="Epsilon for Adam optimizer.")
    parser.add_argument("--max_grad_norm", default=1.0, type=float,
                        help="Max gradient norm.")
    parser.add_argument("--epochs", default=3, type=int,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--warmup_proportion", default=0.1, type=float,
                        help="Proportion of training to perform linear learning rate warmup for, "
                             "E.g., 0.1 = 10% of training.")
    parser.add_argument("--earlystop_patience", default=2, type=int,
                        help="The patience of early stop")
    parser.add_argument('--logging_steps', type=int, default=10,
                        help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=1000,
                        help="Save checkpoint every X updates steps.")
    parser.add_argument('--seed', type=int, default=2021,
                        help="random seed for initialization")
    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    args.output_dir = os.path.join(args.output_dir, args.task_name)
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    args.output_dir = os.path.join(args.output_dir, args.model_name)
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)


    logger = init_logger(os.path.join(args.output_dir, f'{args.task_name}_{args.model_name}.log'))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    args.device = device
    seed_everything(args.seed)

    if 'albert' in args.model_name:
        args.model_type = 'albert'
    tokenizer_class, model_class = MODEL_CLASS[args.model_type]

    # # phase 1
    # # ER process
    # tokenizer = tokenizer_class.from_pretrained(os.path.join(args.output_dir, 'er'))
    
    # ngram_dict = None
    # if args.model_type == 'zen':
    #     ngram_dict = ZenNgramDict(os.path.join(args.model_dir, args.model_name), tokenizer=tokenizer)
    
    # data_processor = ERDataProcessor(root=args.data_dir)
    # test_samples = data_processor.get_test_sample()
    # test_dataset = ERDataset(test_samples, data_processor=data_processor, tokenizer=tokenizer,
    #                          mode='test', max_length=args.max_length, ngram_dict=ngram_dict,
    #                          model_type=args.model_type)
    # model = ERModel(model_class, encoder_path=os.path.join(args.output_dir, 'er'))
    # model.load_state_dict(torch.load(os.path.join(args.output_dir, 'pytorch_model_er.pt')))
    # trainer = ERTrainer(args=args, model=model, data_processor=data_processor,
    #                     tokenizer=tokenizer, logger=logger, model_class=ERModel, ngram_dict=ngram_dict)
    
    # trainer.predict(test_dataset, model)

    # # phase 2
    # json_union(os.path.join('./data/output/ie/robert_base', 'CMeIE_test.json'), os.path.join('./data/result_output', 'CMeEE_test_NER.json'), os.path.join('./data/output/ie/robert_base', 'CMeRE_test.json'))
    # os.remove(os.path.join('./data/output/ie/robert_base', 'CMeIE_test.json'))
    # os.rename(os.path.join('./data/output/ie/robert_base', 'CMeRE_test.json'), os.path.join('./data/output/ie/robert_base', 'CMeIE_test.json'))

    # phase 3 RE
    tokenizer = tokenizer_class.from_pretrained(os.path.join(args.output_dir, 're'))
    tokenizer.add_special_tokens({'additional_special_tokens': ['<s>', '</s>', '<o>', '</o>']})
    
    ngram_dict = None
    if args.model_type == 'zen':
        ngram_dict = ZenNgramDict(os.path.join(args.model_dir, args.model_name), tokenizer=tokenizer)
    
    data_processor = REDataProcessor(root=args.data_dir)
    test_samples = data_processor.get_test_sample(os.path.join(args.output_dir, 'CMeIE_test.json'))
    
    config = None
    if args.model_type == 'zen':
        config = ZenConfig.from_json_file(os.path.join(args.output_dir, 're', 'config.json'))
        config.vocab_size += 4

    model = REModel(tokenizer, model_class, os.path.join(args.output_dir, 're'),
                    num_labels=data_processor.num_labels, config=config)
    model.load_state_dict(torch.load(os.path.join(args.output_dir, 'pytorch_model_re.pt')))
    trainer = RETrainer(args=args, model=model, data_processor=data_processor,
                        tokenizer=tokenizer, logger=logger, model_class=REModel, ngram_dict=ngram_dict)
    
    trainer.predict(test_samples=test_samples, model=model, re_dataset_class=REDataset)

if __name__ == '__main__':
    main()
