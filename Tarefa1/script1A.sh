for nome in `cut -d':' -f3 AV1.txt | cut -d'.' -f2-3 | cut -d'-' -f1 | sort | uniq`
do
  contador=`cat AV1.txt | grep $nome | wc -l`
  echo -e $nome ',' $contador 
done 
