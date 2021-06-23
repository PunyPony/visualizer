from django import forms

class Display(forms.Form):
    file_name = forms.CharField(label='file_name', max_length=100, required=True)
    func = forms.CharField(label='func', max_length=100, required=True)
    axis = forms.CharField(label='axis', max_length=1, required=False)
    use_mask = forms.BooleanField(label="use_mask", required=False)
    slice_nb = forms.IntegerField(label="slice_nb", required=False)
