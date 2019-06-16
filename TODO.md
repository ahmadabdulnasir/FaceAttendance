res{
w:341,h:401
}

main{
w:431,h:401
}

# Draw a rectangle around the faces
# Transparency
def addTranparency(np_img, rect, msg)
  overlay = fram.copy()
  alpha = 0.4  # Transparency factor.
  color = (255, 0, 0)
  y = 10
  cv2.rectangle(overlay, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), -1) #frame -> overlay
  cv2.putText(overlay, msg, ( rect[0]+8, rect[1]+20 + y  ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color , 2 )
  fram = cv2.addWeighted(overlay, alpha, fram, 1 - alpha, 0)
return fram
