def is_sum(check_num, preceding_nums):
    for number_1 in preceding_nums:
        for number_2 in preceding_nums:
            if(number_1 != number_2 and (number_1 + number_2) == check_num):
                return True;
    return False;

def find_number_exception(preceding_range, numbers) -> int :
    for i in range(preceding_range, len(numbers)):
        if(not is_sum(numbers[i], numbers[(i-preceding_range):i])):
            return numbers[i];
    return 0;

file = open("ppp-2023/data/input_sequence.txt", "r")
data_str = file.read()
file.close()
assert(find_number_exception(25,[int(string) for string in data_str.split("\n") if string != ""]) == 1639024365)

def getNumber(string):
    i = 0
    for c in string:
        if(c.isdigit()): i=i+1
    if(i):
        number = 0
        try:
            number = int(string[:i])
        except:
            return 1
        return number
    else:
        return 1

def rec_count(item,complete_bag):
    return (0 if not complete_bag[item] else
    (sum(value+value*rec_count(bags,complete_bag) for value,bags in complete_bag[item])))

def count_bags_inside(parsed_bag={}):
    file = open("ppp-2023/data/input_bags.txt", "r")
    data_str = file.read()
    file.close()
    for string in data_str.split("\n"):
        bag, contents = string.replace(" bags","").replace(" bag","").split(' contain ')
        if("no other" not in contents):
            parsed_bag[bag] = [(getNumber(bags),bags[len(str(getNumber(bags))) :]
            .strip()) for bags in contents.rstrip(".").split(", ")]
        else:
            parsed_bag[bag] = []
    return rec_count("shiny gold", parsed_bag)

assert(count_bags_inside() == 6260)

def count_bags_one_line(pbag={}):return(count("shiny gold",pbag)
if((count:=lambda bag,cbag:(0if not cbag[bag]
else sum(val+val*count(ibag,cbag)
for(val,ibag)in cbag[bag])))and(data:=open("data.txt","r"))
and(dstr:=data.read())and(not data.close())
and(_:=[pbag.update({bag[:-5]:[(ilen:=(int(cont[:sum([1for(cchar)
in(cont)if cchar.isdigit()])])if(sum([1for(cchar)in(cont)
if cchar.isdigit()])!=0)else 1),cont[len(str(ilen)):].strip())
for(cont)in conts.replace(" bags","").replace(" bag", "").rstrip(".")
.split(", ")] if"no other bags"not in conts else[]})
for(bag,conts)in[string.strip().split(" contain ")
for(string)in dstr.split("\n")]]))else 0)

#compressed:
def c(a,h,s,x,z,q,u,o,p,y,t,v,w,r,ab,ac,ad,ae):return(b(r,a)
if(b:=lambda d,e:(q(g+g*b(f,e)for(g,f)in e[d])if e[d]else 0))
and(i:=t(h))and(not v(h))and([w(a)({j[:-5]:[(k:=(y(l[:q([1for(m)in(l)if
u(m)])])if(q([1for(m)in(l)if u(m)])!=0)else 1),x(l[o(p(k)):])())for(l)in
s(x(z(z(n,ab),ac))("."))(", ")]if(ae)not in(n)else[]})for(j,n)in[s(x(o)())(ad)
for(o)in s(i)("\n")]])else 0)

assert(c({},open("data.txt","r"),lambda x:x.split,lambda y:y.strip,
lambda x,y:x.replace(y,""),sum,lambda x:x.isdigit(),len,str,int,
lambda x:x.read(),lambda x:x.close(),lambda x:x.update,"shiny gold",
" bags"," bag"," contain ","no other bags") == 6260)
