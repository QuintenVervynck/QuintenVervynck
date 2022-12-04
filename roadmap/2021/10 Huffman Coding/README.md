# Huffman coding

In this year's project for algorithms and datastructures,
we are investigating whether it is a good idea to allow multiple characters per leaf in an
adaptive huffman compression tree to allow multiple characters per leaf. For instance, there
for example, there could be a leaf representing the character sequence `oe`. We
will implement the algorithm and look at the performance in time and
space of implementations with more or fewer characters per leaf.

## Design decisions & implementation choices
I started with a fairly basic implementation of adaptive huffman encoding. That is, we create nodes that track the necessary attributes for each node (weight, order-number, children (left and right), parent and the group of characters).
 
_We now discuss implementation choices and changes to the above, standard, algorithm._

##### Do not store order-numbers explicitly
As a first change, we no longer store the order-number of a node, but instead we keep a (single) linked list going from highest to lowest order-number.

We do this by adding the right child (which contains the group of characters) to the back of the list first, and then the left child (the new not yet seen) each time we want to add a character - thus creating 'the little Huffman tree'.
 
Note that the old nng (or parent in the small added tree) is now at 3rd last position in the list, the right child at 2nd last position and the new 'not yet seen' at last position. This corresponds to the order-numbers we would normally store in the node itself. Furthermore, we note that the order-numbers are now correct, without having to explicitly increment all order-numbers outside the small tree.
 
When we now look for a node with equal weight and maximum order, we can traverse the list from highest to lowest. The first node we encounter with the correct weight is also immediately the node with the highest order-number.


##### A hash table for leaves (for nodes containing a group of characters)
A hash table of 256 in size - for every possible value of 1 byte (2 to the 8th power), there is 1 spot in the table - seemed an obvious choice for beforehand unknown types of files.

The hash function is then - again quite simpel - the first byte of the group of characters in the node (which in the C programming language corresponds to the first char of the group).

For each entry in the table, we then create a (single) linked list of the nodes that have that byte as the first byte in their group of characters. There is no explicit order in the linked list.
 
Now, when we want to see if a particular group of characters is in the tree, we look at the first byte of the group. We use this value as an index in the table, and then traverse the linked list located at that index.

##### Memory usage
Total memory usage was measured by constructing a huffman tree containing all possible characters (bit sequences 1 byte long). We consider this to be the minimum memory required (69 MiB). Anything left over may be used by the character-distribution heuristic to create, say, a node of 2 or 3 characters.

Thus, if the heuristic has used up all the remaining memory, it is guaranteed that the file can still be compressed (because there is enough memory to encode every possible character separately, i.e. in 'groups' of 1 character in size.

Note that the heuristics will thus never encode nodes with 1 character. This choice was made because the study deals with multiple characters per node. It only switches strategies - to 1 character per node - in order to guarantee compression of any file.


## Character-distribution heuristics
We will now discuss some heuristics and compare their compression ratios. 
Each of the heuristics will be tested on a few different files. 

- A first file represents an English text of great length, it is the script of the first Star Wars film of the Skywalker saga. [(view the script)](https://imsdb.com/scripts/Star-Wars-The-Phantom-Menace.html)
- A second file contains completely random bytes. So the diversity is much greater here than in the previous file. There will be hardly any correlation between consecutive bytes.
 - A third file contains a short 1-sentence chat message. It is 72 bytes in size and contains 13 words.

#### Add max
Set n the maximum size of a character group. Add group of n characters. 
 
We now look at the graph below showing the compression for this heuristic.

<img src="posts/2021/huffman_graph_add_max_english_text.png" alt="huffman_graph_add_max_english_text" style="width:70%;"/>

We see that the compression is highest for groups of 2 characters, if we allow our programme to use a maximum of 1 MiB of memory.


#### Add random
Set n to be the maximum size of a character group. 

1. Randomly generate a number i between 2 and n (inclusive bounds). 
2. Add the following i characters in one group

Repeat steps 1 and 2 until all characters are encoded
 
We now look at the graph below that shows the compression for this heuristic.

<img src="posts/2021/huffman_graph_add_random_english_text.png" alt="huffman_graph_add_random_english_text" style="width:70%;"/>

We see no difference for the best compression (group size 2 with maximum memory of 1 MiB). 

For group sizes 3 to 9, the compression ratios are slightly lower than for the add max heuristic.


#### Add scaled
Set n the maximum size of a character group
1. Generate a random number i between 2 and n (inclusive bounds).
1. Add the next i characters in one group and keep doing this until the already added characters + i would be larger than the maximum size of a character group.

Some examples: 
- if n=8 and i=2 then 4 groups of 2 characters will be added
- if n=8 and i=2 then 2 groups of 4 characters will be added


The bottom line is that more smaller groups will be added. In other words, a kind of scaling factor has been added that will favour encoding smaller groups.
 
We now look at the graph below which shows the compression for this heuristic.

<img src="posts/2021/huffman_graph_add_scaled_english_text.png" alt="huffman_graph_add_scaled_english_text" style="width:70%;"/>

We see a graph similar to that of the add random heuristic. Note that both for this heuristic, and the 2 previous ones, it is possible to make the file larger during encoding.


#### Find subset
All previous heuristics did not actually take into account what is already in the tree. Hence, the incomplete heuristic 'find subset' is introduced here. I call it incomplete because it will only do something if a subset of the current group of characters is already in the tree; if it is not, we can have another heuristic follow it. We now discuss how it works.
 
Assume n is the maximum size of a character group.

Set i equal to n, repeat the following steps as long as i > 1

1. find the group of characters [0, i-1] in the tree, with 0 being the first current character (so the group will have length i)
1. if this character group is in the tree -> encode this group and stop
2. otherwise, set i equal to i -1 and repeat steps 1-3 as long as i > 1

If - at the end of the loop - no character group was encoded, then we use 1 of the other heuristics to add new character groups.
 
The combinations of the previous heuristics with this find subset will now be discussed.

#### Find subset with add max
This is the combination of the heuristics find subset and add max.

We immediately look at the results.

<img src="posts/2021/huffman_graph_find_subset_add_max_english_text.png" alt="huffman_graph_find_subset_add_max_english_text" style="width:70%;"/>

There is no difference with the regular add max, this is because never other sizes of groups of characters will appear in the huffman tree. So the find subset has no effect here.

#### Find subset with add random
This is the combination of the heuristics find subset and add max.

We immediately look at the results.

<img src="posts/2021/huffman_graph_find_subset_add_random_english_text.png" alt="huffman_graph_find_subset_add_random_english_text" style="width:70%;"/>

We see here that all group sizes are equally or better than the adaptive huffman with 1 character per leaf. The best compression here is achieved with a group size of 4 (for group size 3, the compression is only 0.009 lower) with a maximum memory of 1 MiB). 

Note that here we have no encodings that make the file larger.

#### Find subset with add scaled
This is the combination of the heuristics find subset and add max.

We immediately look at the results.

<img src="posts/2021/huffman_graph_find_subset_add_scaled_english_text.png" alt="huffman_graph_find_subset_add_scaled_english_text" style="width:70%;"/>

We see a similar graph to find subset add random. But the maximum compression is now obtained with group size 3 and a maximum memory of 1 MiB

## What about the compression of a chat message or random data?
For the chat message and random data, very poor compression ratios were obtained. We discuss them below on the best-performing heuristic (find subset with add random).

With the chat message, the problem is that the file is too small to achieve real compression. In this case, it would be better to work with a group of chat messages and build a Huffman tree based on them. Which chat messages are best grouped together is beyond the scope of this study.

With the random data, diversity is the problem. Characters do not repeat themselves often enough, and thus compression cannot be obtained.


## Conclusion
The heuristic that performed best was find subset with add random, with a group size of 4 and a memory limit of 1 MiB. For small files (vb chat messages) or completely random data, it is best not to use adaptive huffman. So the file should not be too small, and it should contain some form of repetition (some characters (or groups) should appear more often than others). 

But all in all, it is possible to use a group size larger than 1 and smaller than 5 if one has the system requirements for it and considers compression ratio as the most important factor. But for very small systems, it would be best to use group size 1.
 
