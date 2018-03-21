#!/bin/bash

data_dir='./data/'

stock_id_str=`echo ${stock_id_str} | sed "s/,/ /g" `
if [ "X$1" != "X" ];then
	org_file=${data_dir}"$1"
else
	org_file=${data_dir}'sina_data'
fi

if [ "X$2" != "X" ];then
	stock_id_str=$2
else
	stock_id_str='000300,000016,000905'
fi

stock_id_str=`echo ${stock_id_str} | sed "s/,/ /g" `

for stock_id in ${stock_id_str}
do
	output_file=${data_dir}"${stock_id}"
	grep ${stock_id} ${org_file} | awk -F ',' '{OFS=","}{print $2,$3,$4,$5,$6}' | sort >${output_file}
	output_file_lines=`cat  ${output_file} | wc -l `
	echo "fetch code ${stock_id} to file ${output_file}, lines: ${output_file_lines}"
	sed -i '1i\price_date,open_price,highest_price,lowest_price,close_price' ${output_file}
done
