BITMASK=[0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]
g_width=12
g_planet={}
g_planet['Sun']=bytearray([
      0x60, 0x00, 0x9c, 0x03, 0x02, 0x04, 0x02, 0x04, 0x02, 0x04, 0x61, 0x08,
   0x61, 0x08, 0x02, 0x04, 0x02, 0x04, 0x02, 0x04, 0x9c, 0x03, 0x60, 0x00])
g_planet['Moon']=bytearray([
      0x3c, 0x00, 0xc8, 0x00, 0x10, 0x01, 0x20, 0x02, 0x20, 0x02, 0x40, 0x04,
   0x40, 0x04, 0x20, 0x02, 0x20, 0x02, 0x10, 0x01, 0xc8, 0x00, 0x3c, 0x00])
g_planet['Mercury']=bytearray([
       0x04, 0x01, 0x88, 0x00, 0x70, 0x00, 0x8c, 0x01, 0x04, 0x01, 0x02, 0x02,
   0x04, 0x01, 0x8c, 0x01, 0x70, 0x00, 0x20, 0x00, 0xfc, 0x01, 0x20, 0x00])
g_planet['Venus']=bytearray([
     0x70, 0x00, 0x8c, 0x01, 0x04, 0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02,
   0x04, 0x01, 0x8c, 0x01, 0x70, 0x00, 0x20, 0x00, 0xf8, 0x00, 0x20, 0x00])
g_planet['Mars']=bytearray([
      0x80, 0x07, 0x00, 0x06, 0x00, 0x05, 0xb8, 0x04, 0xc6, 0x00, 0x82, 0x00,
   0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x82, 0x00, 0xc6, 0x00, 0x38, 0x00])
g_planet['Jupiter']=bytearray([
       0x06, 0x01, 0x08, 0x01, 0x10, 0x01, 0x20, 0x01, 0x20, 0x01, 0x20, 0x01,
   0x10, 0x01, 0x08, 0x01, 0xfe, 0x07, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01])
g_planet['Saturn']=bytearray([
     0x04, 0x00, 0x1f, 0x00, 0x04, 0x00, 0x64, 0x00, 0x94, 0x01, 0x0c, 0x02,
   0x04, 0x04, 0x00, 0x04, 0x00, 0x04, 0x00, 0x02, 0x00, 0x01, 0xc0, 0x00 ])
g_planet['Uranus']=bytearray([
     0x01, 0x04, 0x22, 0x02, 0x24, 0x01, 0xfc, 0x01, 0x24, 0x01, 0x22, 0x02,
   0x71, 0x04, 0x88, 0x00, 0x04, 0x01, 0x04, 0x01, 0x88, 0x00, 0x70, 0x00])
g_planet['Neptune']=bytearray([
  0x20, 0x00, 0x70, 0x00, 0x22, 0x02, 0x27, 0x07, 0x22, 0x02, 0x22, 0x02,
   0x24, 0x01, 0xa8, 0x00, 0x70, 0x00, 0x20, 0x00, 0xf8, 0x00, 0x20, 0x00])    
g_planet['Pluto']=bytearray([
      0x70, 0x00, 0x88, 0x00, 0x04, 0x01, 0x04, 0x01, 0x89, 0x04, 0x71, 0x04,
   0x02, 0x02, 0x8c, 0x01, 0x70, 0x00, 0x20, 0x00, 0xf8, 0x00, 0x20, 0x00])


    
def test(tft):
    from color import NAVY,WHITE
    bs = g_planet['Sun']
    h = int(len(bs)/2.0)
    nbs = conv_mono2_to_rgb565(bs,NAVY,WHITE)
    tft.blit_buffer(nbs,10,10,12,h)
