"""Running the Xetra ETL app"""
import argparse
import logging
import logging.config
import yaml

from xetra.common.s3 import S3BucketConnector
from xetra.transformers.xetra_transformer import XetraETL, XetraSourceConfig, XetraTargetConfig


def main():
    """
    entry point to run the ETL job
    """
    # Parsing YAML file
    parser = argparse.ArgumentParser(description='Run the Xetra ETL job.')
    parser.add_argument('config', help='A configuration file in YAML format.')
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))

    # configure logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)

    # reading s3 configure
    s3_config = config['s3']
    # creating the S3BucketConnector class instance
    s3_bucket_src = S3BucketConnector(access_key=s3_config['access_key'],
                                        secret_key=s3_config['secret_key'],
                                        endpoint_url=s3_config['src_endpoint_url'],
                                        bucket=s3_config['src_bucket'])
    s3_bucket_trg = S3BucketConnector(access_key=s3_config['access_key'],
                                        secret_key=s3_config['secret_key'],
                                        endpoint_url=s3_config['trg_endpoint_url'],
                                        bucket=s3_config['trg_bucket'])

    # reading source config
    source_config = XetraSourceConfig(**config['source'])
    # reading target config
    target_config = XetraTargetConfig(**config['target'])
    # reading meta file config
    meta_config = config['meta']

    #creating XetraETL
    logger.info('Xetra ETL job started')
    xetra_etl = XetraETL(s3_bucket_src, s3_bucket_trg,
                        meta_config['meta_key'], source_config, target_config )
    # running etl job 
    xetra_etl.etl_report1()
    logger.info('Xetra ETL job finished')
    
if __name__ == '__main__':
    main()
    