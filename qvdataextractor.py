import os
import json

from qlikreader.qlikreader import QlikReader

from system_fields import Host as QVHost
from system_fields import WaitTime as WT
from system_fields import QVMetrics as QVM
from system_fields import BOOKMARK

#from config import DEBUG
#from config import MONGO_DATABASE_NAME

driver_dir = os.path.dirname(os.path.dirname(os.path.realpath('__file__')))

# ToDo verify and cleanup
# web_driver_path = os.path.join(driver_dir, 'wsgi/webdriver/chromedriver')

web_driver_path = os.path.join(driver_dir, 'webdriver/chromedriver')

os.environ['webdriver.chrome.driver'] = web_driver_path

ops_out_dir = os.path.join(os.path.dirname(driver_dir), 'data')

user = os.environ['QVUSERNAME']

pwd = os.environ['QVPASSWORD']

qvbase_url = 'https://'+user+':'+pwd+'@'+QVHost

locate_element = "TextObject"

locate_element_xpath = "/html/body/div[3]/div/div[1]/div[2]/table/tbody/tr/td"


def qvextractor():
    """
    :return:
    """

    for metrics in QVM:

        metrics_out_file = os.path.join(ops_out_dir, metrics) + '.json'

        with open(metrics_out_file, "wb") as outfile:

            master_out_dict = {}

            for obj in QVM[metrics]:

                out_dict = {}

                obj_id = QVM[metrics][obj]

                for fy_book_mark in BOOKMARK:

                    qvurl = qvbase_url+\
                            "QvAJAXZfc/singleobject.htm?document=Marketing%20Application%20Folder/Lead_Process.qvw&host=QVS@phx2-qlikview01&object="+\
                            obj_id+\
                            "&bookmark="+fy_book_mark[1]

                    qr_driver = QlikReader()

                    qr_driver.init_driver(web_driver_path, WT, qvurl)

                    mertrics_obj_val = qr_driver.lookup(locate_element, locate_element_xpath)

                    if mertrics_obj_val:

                        mertrics_obj_val=int((mertrics_obj_val).replace(',', ''))

                    mertrics_key = 'cfy' if fy_book_mark[0] == 'current_fy' else 'lfy'

                    out_dict[mertrics_key] = mertrics_obj_val

                    qr_driver.quit_driver()

                master_out_dict[obj] = out_dict

                #print out_dict

            json.dump(master_out_dict, outfile)


if __name__ == "__main__":
    # Call pull_properties_data method to pull data and load it into db.
    qvextractor()
