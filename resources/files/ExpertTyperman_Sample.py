import time

n = 10
for i in range(n):
    print(f'\r/!\\ Uploading Virus... [{100*i/n:.2f}%]', end='')
    time.sleep(0.2)
print('\rDone!')