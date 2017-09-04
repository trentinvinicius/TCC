#! /bin/env python
import sys, os, time
import pymedia.video.vcodec as vcodec
import pygame

class VideoWriter():
    def Init(self, outavi, width, height, framerate, outCodec="mpeg1video"):
        pygame.init()
        self.e = None
        self.fw= open( outavi, 'wb' )
        if outCodec== 'mpeg1video':
          bitrate= 2700000
        else:
          bitrate= 9800000

        params= { \
          'type': 0,
          'gop_size': 12,
          'frame_rate_base': 125,
          'max_b_frames': 0,
          'height': height,
          'width': width,
          #'frame_rate': 2997,
          'frame_rate': framerate,
          'deinterlace': 0,
          'bitrate': bitrate,
          'id': vcodec.getCodecID( outCodec )
        }
        self.e= vcodec.Encoder( params )
        #t= time.time()

    def WriteFrame(self, filename):
        s= pygame.image.load( filename)
        ss= pygame.image.tostring(s, "RGB")
        bmpFrame= vcodec.VFrame( vcodec.formats.PIX_FMT_RGB24, s.get_size(), (ss,None,None))
        yuvFrame= bmpFrame.convert( vcodec.formats.PIX_FMT_YUV420P )
        d= self.e.encode( yuvFrame )
        #print d.data
        #fw.write( d )
        self.fw.write( d.data )

    def Close(self):
        self.fw.close()
        pygame.quit()

