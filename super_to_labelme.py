
import json
import argparse

#TODO: Add multi file processing (This solution only works for one json file).

class LabelmeDset:
  def __init__(self, input_files=[]):
    """
      This Object is used to convert one or more supervisly files
      into labelme format.

      params: 

      arg1(input_files) : This is a list of one or more json files
      you want to convert to labelme format.

      example:
            dset = LabelmeDset(input_files=['rset.json','keset.json'])
            dset(out_file='trainset.json')
    """

    if type(input_files) != list:
      raise Exception('input error, input is expected to be a list of file name(s)')
    self.input_files = input_files
    self.out_values = {
                        'images': [],
                        'annotations' : [],
                        'categories' : []
                      
                      }
    self.image_id = 0
    self.categories_id = 0
    self.labels_id = 0

  def __call__(self,more_input=None,out_file='output.json'):
    """
      This function is called to run the convertion process, 

      arg1(more_input) : This is a list of one or more json files
      you want to add to the previous list of files to be converted
      to labelme format.

      arg2(out_file) : This function expects an argument that specifies 
      the output of the resultant file.
      
      example1:
            dset = LabelmeDset(input_files=['rset.json','keset.json'])
            dset(more_input=['jjset.json'],out_file='trainset.json')

      example2:
            dset = LabelmeDset(input_files=['rset.json','keset.json'])
            dset(more_input=None,out_file='trainset.json')

      example1:
            dset = LabelmeDset(input_files=['rset.json','keset.json'])
            dset(out_file='trainset.json')
    """
    self.input_files = self.input_files+more_input if type(more_input) == list else self.input_files
    self.process_all_inputs(output=out_file)

  def process_all_inputs(self,output=None):
    for each_file in self.input_files:
      file = open(each_file.strip())
      file = json.load(file)

      self.out_values['images'] += self.process_image(file['images'])
      self.out_values['categories'] += self.process_cat(file['categories'])
      self.out_values['annotations'] += self.process_ann(file['annotations'])
    
    self.save_outfile(output)

  def process_image(self,obj_lst=None):
    new_lst = []
    interested_in = ["height", "width", "id", "file_name"]
    for each in obj_lst:
      new_dict = {}
      
      for key,value in each.items():
          if  key in interested_in and key == 'file_name':
            new_dict[key] = value.split('/')[-1]
          elif key in interested_in:
            new_dict[key] = value
      new_lst.append(new_dict)
    return new_lst

  def process_ann(self,obj_lst=None):
    new_lst = []
    interested_in = ["segmentation", "iscrowd", "area", "image_id","bbox","category_id","id"]
    for each in obj_lst:
      new_dict = {}
      
      for key,value in each.items():
          if  key in interested_in and key == 'segmentation':
            value = value[0]
            new_seg = []
            for each_seg1,each_seg2 in value:
              new_seg.append(each_seg1)
              new_seg.append(each_seg2)
            new_dict[key] = [new_seg]
          elif key in interested_in:
            new_dict[key] = value
      new_lst.append(new_dict)
    return new_lst

  def process_cat(self,obj_lst=None):
    new_lst = []
    interested_in = ["supercategory", "id", "name"]
    for each in obj_lst:
      new_dict = {}
      
      for key,value in each.items():
          if  key in interested_in and key == 'name':
            new_dict['name'] = value
          elif key in interested_in:
            new_dict[key] = value
      new_dict["supercategory"] = new_dict['name']
      new_lst.append(new_dict)
    return new_lst

  def save_outfile(self,output_name='output,json'):
    with open(output_name, 'w') as json_file:
      json.dump(self.out_values,json_file, indent=4, separators=(',', ': '))

def main(args):
  dset = LabelmeDset(input_files=args.input_file.split(','))
  dset(out_file=args.output_name)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_name', required=True)
    
    args=parser.parse_args() 
    main(args)