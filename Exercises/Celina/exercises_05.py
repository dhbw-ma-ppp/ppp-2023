# PART 1:
# Here's a sequence of numbers:
# [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
# numbers in this list can in general be expressed as a sum of some pair of two numbers
# in the five numbers preceding them.
# For example, the sixth number (40) cam be expressed as 25 + 15
# the seventh number (62) can be expressed as 47 + 15 etc.
# 
# The only exception to this rule for this example is the number 127.
# The five preceding numbers are [95, 102, 117, 150, 182], and no possible sum of two of those
# numbers adds to 127.
#
# You can find the ACTUAL input for this exercise under `data/input_sequence.txt`. For this
# real input you should consider not only the 5 numbers, but the 25 numbers preceding.
# Find the first number in this list which can not be expressed as a
# sum of two numbers out of the 25 numbers before it.
# Please make not of your result in the PR.

test =  [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

list=[]
text= open("data/input_sequence.txt","r")
for line in text:
    list.append(int(line))
    #print(list)


def find_number(list):
    number = 25
    while number <= len(list):
        temp_list= sorted(list[number-25:number])
        #print (temp_list)
        i=0
        j=24
        sum = temp_list[i] + temp_list[j]
        while list[number] != sum:
            if i==j:
                return list[number]
            elif list[number] < sum:
                j-=1
            elif list[number] > sum:
                i+=1
            sum = temp_list[i] + temp_list[j]
        number+=1

print(find_number(list))

#print(find_number(test))

# PART 2:
# The input to this exercise specifies rules for bags containing other bags.
# It is of the following form:
#
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
#
# You have a single 'shiny gold bag'. Consider the rules above. According
# to those rules your bag contains
# - 1 dark olive bag, in turn containing
#   - 3 faded blue bags (no further content)
#   - 4 dotted black bags (no further content
# - 2 vibrant plum bags, in turn containing
#   - 5 faded blue bags (no further content)
#   - 6 dotted black bags (no further content)
# 
# therefore, your single shiny gold bag contains a total of 32 bags
# (1 dark olive bag, containing 7 other bags, and 2 vibrant plum bags,
# each of which contains 11 bags, so 1 + 1*7 + 2 + 2*11 = 32)
#
# The ACTUAL input to your puzzle is given in `data/input_bags.txt`, and much larger
# and much more deeply nested than the example above. 
# For the actual inputs, how many bags are inside your single shiny gold bag?
# As usual, please list the answer as part of the PR.

bags_dic = {}

word = " contain "

bags= open("data/input_bags.txt","r")
for line in bags:
    input = line.rstrip("\n")
    input_list=input.split(word)
    #print(list)
    bags_dic[input_list[0]]=input_list[1]
#print(bags_dic)

start_bag="shiny gold bags"

def count_it(counter):
    product=1
    for numbers in counter:
        product*=numbers
    return product

def count_bags(bags_dic,start_bag,counter=[1],bag_count=[],recursion_count=1):
    if start_bag in bags_dic:
        bags_list=bags_dic[start_bag].split(",")
        #print ("1:",start_bag,":",bags_list)
        for elements in bags_list:
            #print("2:",elements)
            bag=elements.strip(". ")
            bag=bag.split(" ",1)
            if bag[0] == "no":
                #product=1
                #for numbers in counter:
                    #product*=numbers
                product=count_it(counter)
                #print("4.1:",recursion_count,counter)
                #print("4:",product)
                bag_count.append(product)
                del counter[-1]
                return bag_count
            else:
                number_bags=int(bag[0])
                if len(counter)<=recursion_count:
                    counter.append(1)
                counter[recursion_count]=number_bags
                if number_bags==1:
                    new_start_bag=bag[1] + "s"
                else:
                    new_start_bag=bag[1]
                #print("3:",bag)
                bag_count=count_bags(bags_dic,new_start_bag,counter,bag_count,recursion_count+1)
                count=0
                for elements in bag_count:
                    count+=elements
                #print("done:",count)
                #print("done",start_bag,bag_count)
        if start_bag== "shiny gold bags":
            return bag_count
        product=count_it(counter)
        #print("4.1:",recursion_count,counter)
        #print("4:",product)
        bag_count.append(product)
        del counter[-1]
        return bag_count

def main():
    bag_count=count_bags(bags_dic,start_bag)
    count=0
    for elements in bag_count:
        count+=elements
    print(count)

main()

