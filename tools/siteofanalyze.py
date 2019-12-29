"""

"""
from site_conf.models import *
import re


from rest_framework import  status
from rest_framework.response import Response
from django.db.models import Q


def sql_Select_Get_Columns(technology, sql_syntax):

	SQL_SYNTAX = sql_syntax
	RE_SYMBOLS = r"""[-!$%^&*()+|~=`{}\[\]:";'<>?,.\/]"""
	SQL_METHOD = ['SUM', 'AVG', 'MAX', 'MIN', 'ROUND']
	EX_TABLE = ['']
	
	ALL_COUNTER = {}
	for _counter in kpi_counter.objects.filter(technology=technology):
		if ALL_COUNTER.get(_counter.netact_name.upper(), ''): 
			ALL_COUNTER[_counter.netact_name.upper()].append(re.sub(r'(M\d+).*', r'\1', _counter.counter_id))
		else:
			ALL_COUNTER[_counter.netact_name.upper()] = [re.sub(r'(M\d+).*', r'\1', _counter.counter_id)]

	exist_cols = []
	for col in re.split(RE_SYMBOLS, SQL_SYNTAX):
		if col.upper() not in SQL_METHOD and re.match(r'\D',col) and col:
			if len(ALL_COUNTER[col.upper()]) > 1:
				raise Response("The mutiple counter existing.", status=status.HTTP_400_BAD_REQUEST)
			exist_cols.append(ALL_COUNTER[col.upper()][0])
		
	return ','.join(list(set(exist_cols)))

# define response data format
def resp_Format(li_content, index, fir_col):
	assert isinstance(li_content, list)
	assert isinstance(index, str)
	assert isinstance(fir_col, list)

	result_dict = {}
	for _dict in li_content:
		result_fields = {}
		index_name = _dict[index]
		for key, val in _dict.items():
			if not result_dict.get(index_name, {}):
				result_dict[index_name] = {}
				result_dict[index_name]['fields'] = []

			if key not in fir_col:
				result_fields[key] = val
			else:
				result_dict[index_name][key] = val 
		result_dict[index_name]['fields'].append(result_fields)

	return [result_dict[key] for key in result_dict.keys()]


# response the shared filter
class Resp_Shared_Filter(object):
	def __init__(self, request, model_obj):
		self.request = request
		self.model_obj = model_obj
		self.obj_all_data = model_obj.objects.all()

	def authority_Filter(self, sharedable_obj = ''):
		if self.request.user.is_superuser:
			return self.obj_all_data
		super_user_pk = User.objects.filter(is_superuser=1)
		self.obj_all_data = self.obj_all_data.filter(
				Q(creator_id__in=[_usr.pk for _usr in super_user_pk]) | 
				Q(creator_id=self.request.user.pk)
			)

		if sharedable_obj:
			be_shared_pk = sharedable_obj.objects.filter(
				Q(target_user_id = self.request.user.pk) |
			 	Q(target_group_id__in = self.request.user.groups.all().values())
			 )

	def suggestion_Limit(self):
		limit = self.request.GET.get('suggestion_limit', '')
		try:
			if limit:
				self.obj_all_data  = self.obj_all_data [:int(limit)]
		except Exception as e:
			raise Response('Suggestion_limit parameter is not number.', status=status.HTTP_400_BAD_REQUEST)
		return self.obj_all_data 

	def db_Detail_Filter(self ,allow_params ,isinclude = False):
		assert isinstance(allow_params, list)

		get_params = self.request.GET

		get_params = {key:val[0]  for key, val in dict(get_params).items() if key in allow_params}
		if not get_params:
			return 'No allow parameter in get.'
		kpi_counter_cols = [obj.name for obj in self.model_obj._meta.get_fields()]

		if isinclude:
			filter_val= {key+'__icontains':val for key,val in get_params.items() if key in kpi_counter_cols}
		else:
			filter_val= {key:val for key,val in get_params.items() if key in kpi_counter_cols}

		if filter_val:
			self.obj_all_data = self.obj_all_data.filter(**filter_val)

		return self.obj_all_data

