print(sum(complex((c<=a<=b<=d)|(a<=c<=d<=b),(c<=b)&(a<=d))for a,b,c,d in[map(int,x.replace(",","-").split("-"))for x in open("d").read().splitlines()]))