from database import Mysql
import csv


def text_rank():
    # 划分文件完整性等级
    db_r = Mysql('root','990211','dbpolicy',use_flow=True)
    db_w = Mysql('root','990211','dbpolicy')

    for item in db_r.select('data','code,gov,source,title,date,main_text,attachment,img'):
        insert_dict = {'code':item['code'],'gov':item['gov'],'source':item['source'],'title':item['title'],'date':item['date']}
        if item['main_text'] and len(item['main_text']) > 20:
            insert_dict['rank'] = 1
        elif item['attachment']:
            insert_dict['rank'] = 2
        elif item['img']:
            insert_dict['rank'] = 3
        else:
            insert_dict['rank'] = 4
        db_w.insert_one('text_rank',insert_dict)


def search_main_text():
    # 根据文件名查找文件正文等完整信息
    db = Mysql('root','990211','dbpolicy')
    with open('./data/label_text.csv','r',encoding='utf-8-sig') as fr:
        csv_r = csv.DictReader(fr)
        for line in csv_r:
            print(line)
            result = db.select('data','main_text','title = "{}" and gov="{}" and code = "{}"'
                               .format(line['title'],line['gov'],line['code']),fetch_one=True)
            if result:
                tmp_dict = {'title':line['title'],'text':result['main_text'],'label':line['label']}
                with open('./data/train_data.csv','a',encoding='utf-8-sig',newline='') as fa:
                    csv_a = csv.DictWriter(fa,fieldnames=['title','text','label'])
                    csv_a.writerow(tmp_dict)
            
            
if __name__ == '__main__':
    search_main_text()