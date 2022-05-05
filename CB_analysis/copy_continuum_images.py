import os

for i in range(0,10):
	os.popen('cp /data/apertif/200102012/{:02}/continuum/*mf*.fits /tank5/denes/continuum_images/continuum_b{:02}.fits'.format(i,i))
	
for i in range(10,20):
	os.popen('cp /data2/apertif/200102012/{:02}/continuum/*mf*.fits /tank5/denes/continuum_images/continuum_b{:02}.fits'.format(i,i))
	
for i in range(20,30):
	os.popen('cp /data3/apertif/200102012/{:02}/continuum/*mf*.fits /tank5/denes/continuum_images/continuum_b{:02}.fits'.format(i,i))
	
for i in range(30,40):
	os.popen('cp /data4/apertif/200102012/{:02}/continuum/*mf*.fits /tank5/denes/continuum_images/continuum_b{:02}.fits'.format(i,i))