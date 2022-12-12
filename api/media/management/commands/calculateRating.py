from django.core.management.base import BaseCommand, CommandError
from media.models import Channel, Content
import time, datetime

class Command(BaseCommand):
  help = 'Generates a CSV File with the rating of each channel.'
  channelRatings = {}

  def add_arguments(self, parser):
    parser.add_argument('-o', '--output', type=str, help='Where the CSV file will be saved.')

  def handle(self, *args, **kwargs):
    # get the output path or filename
    output = kwargs['output']
    if not output:
      output = "ratings_%s.csv" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # start the timer
    start_time = time.time()

    # get all the channels with no parents (Top Level Channels)
    topLvLChannels = Channel.objects.filter(parent=None)

    # loop over each channel and calculate it's rating
    for channel in topLvLChannels:
      # calculate the rating for this channel
      self.calculateChannelRating(channel=channel)

    # generate a CSV file from the dict
    self.generateCSVData(output)

    # check how long it took to generate all the ratings
    print("Ratings calculated in %.2f seconds" % (time.time() - start_time))

  def calculateChannelRating(self, channel: Channel):
    # append channel title to the channelRatings with default value
    self.channelRatings[channel.title] = 0
    
    # get all the channels inside this 
    subChannels = Channel.objects.filter(parent=channel)
    # loop over all subChannels 
    for subChannel in subChannels:
      
      # calculate the rating for the subChannel
      self.calculateChannelRating(subChannel)
      
      # add the subChannel rating to the current channel rating
      self.channelRatings[channel.title] += self.channelRatings[subChannel.title]
    
    # get all the content inside this channel
    contents = Content.objects.filter(channel=channel)
    # loop over contents
    for content in contents:
      # sum the content rating value to the channel rating
      self.channelRatings[channel.title] += content.rating
  
  def generateCSVData(self, output):
    # open the file in write mode
    with open(output, 'w') as csv:
      # add headers
      csv.write("Channel Title,Rating\n")
      # loop over each rating and append it to the file
      for title in self.channelRatings.keys():
        csv.write("%s,%.2f\n" % (title, self.channelRatings[title]))