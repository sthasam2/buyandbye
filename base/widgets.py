from django.forms import DateInput

class FengyuanChenDatePickerInput(DateInput):
    template_name = 'widget/fengyuanchen_datepicker.html'