import random
import datetime


# created_on = datetime.datetime.now()
# print(created_on)
import random
import time
# def getRandomDate(startDate, endDate ):
#     print("Printing random date between", startDate, " and ", endDate)
#     randomGenerator = random.random()
#     dateFormat = '%Y-%m-%d'
#     startTime = time.mktime(time.strptime(startDate, dateFormat))
#     endTime = time.mktime(time.strptime(endDate, dateFormat))
#     randomTime = startTime + randomGenerator * (endTime - startTime)
#     randomDate = time.strftime(dateFormat, time.localtime(randomTime))
#     return randomDate
# print ("Random Date = ", getRandomDate("2016-1-1", "2019-1-1"))

#vypise vsechny verejne udaje z tabulky family,approval_type,family_parent, child_in_care
    # query="""SELECT file_number, at.name AS approval_type, regional_office_id, expectation_status_id, region_id, district_id, carer_info_id, prepcourse, account_id
    #         FROM public.family as f
    #         LEFT JOIN public.approval_type AS at ON f.approval_type_id = at.id
    #         LEFT JOIN public.family_parent AS fp ON f.
    #         ORDER BY region_id;"""

districty=range(1,78)
print(districty)
