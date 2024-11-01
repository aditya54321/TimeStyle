from django.shortcuts import render,redirect
import subprocess
import glob
from .auto_mail import send_smtp_oauth, create_mail_content





def email_script(request):
    # Search for files
    # pattern = '**\\auto_mail.py'    
    # files = glob.glob(pattern, recursive=True)
    # for file in files:
    #     print(file)  
    #     result = subprocess.run(['python', file], 
    #                         capture_output=True, text=True)
    #     output = result.stdout
    #     break
    subject, e_body = create_mail_content()
    send_smtp_oauth("adityasingha.4321@gmail.com", subject, e_body)
    return redirect('home')

    # return render(request,'run_script.html',{'output': f"<pre>{output}</pre>"})

