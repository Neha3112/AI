{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "id": "vuKEoAFody7S"
   },
   "outputs": [],
   "source": [
    "# Global variable kb (knowledge base)\n",
    "kb = []\n",
    "\n",
    "# Reset kb to an empty list\n",
    "def CLEAR():\n",
    "    global kb\n",
    "    kb = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "id": "Ype-utiRdy7S"
   },
   "outputs": [],
   "source": [
    "# Insert sentence to the kb\n",
    "def TELL(sentence):\n",
    "    global kb\n",
    "    # If the sentence is a clause, insert directly.\n",
    "    if isClause(sentence):\n",
    "        kb.append(sentence)\n",
    "    # If not, convert to CNF, and then insert clauses one by one.\n",
    "    else:\n",
    "        sentenceCNF = convertCNF(sentence)\n",
    "        if not sentenceCNF:\n",
    "            print(\"Illegal input\")\n",
    "            return\n",
    "        # Insert clauses one by one when there are multiple clauses\n",
    "        if isAndList(sentenceCNF):\n",
    "            for s in sentenceCNF[1:]:\n",
    "                kb.append(s)\n",
    "        else:\n",
    "            kb.append(sentenceCNF)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "id": "ynHcijLtdy7S"
   },
   "outputs": [],
   "source": [
    "# 'ASK' the kb whether a sentence is True or not\n",
    "def ASK(sentence):\n",
    "    global kb\n",
    "\n",
    "    # Negate the sentence, and convert it to CNF accordingly.\n",
    "    if isClause(sentence):\n",
    "        neg = negation(sentence)\n",
    "    else:\n",
    "        sentenceCNF = convertCNF(sentence)\n",
    "        if not sentenceCNF:\n",
    "            print(\"Illegal input\")\n",
    "            return\n",
    "        neg = convertCNF(negation(sentenceCNF))\n",
    "\n",
    "    # Insert individual clauses that we need to ask to ask_list.\n",
    "    ask_list = []\n",
    "    if isAndList(neg):\n",
    "        for n in neg[1:]:\n",
    "            nCNF = makeCNF(n)\n",
    "            if type(nCNF).__name__ == 'list':\n",
    "                ask_list.insert(0, nCNF)\n",
    "            else:\n",
    "                ask_list.insert(0, nCNF)\n",
    "    else:\n",
    "        ask_list = [neg]\n",
    "# Create a new list combining the asked sentence and kb.\n",
    "    # Resolution will happen between the items in the list.\n",
    "    clauses = ask_list + kb[:]\n",
    "\n",
    "    # Recursivly conduct resoltion between items in the clauses list\n",
    "    # until it produces an empty list or there's no more pregress.\n",
    "    while True:\n",
    "        new_clauses = []\n",
    "        for c1 in clauses:\n",
    "            for c2 in clauses:\n",
    "                if c1 is not c2:\n",
    "                    resolved = resolve(c1, c2)\n",
    "                    if resolved == False:\n",
    "                        continue\n",
    "                    if resolved == []:\n",
    "                        return True\n",
    "                    new_clauses.append(resolved)\n",
    "\n",
    "        if len(new_clauses) == 0:\n",
    "            return False\n",
    "\n",
    "        new_in_clauses = True\n",
    "        for n in new_clauses:\n",
    "            if n not in clauses:\n",
    "                new_in_clauses = False\n",
    "                clauses.append(n)\n",
    "\n",
    "        if new_in_clauses:\n",
    "            return False\n",
    "    return False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "id": "VN1sg1jjdy7S"
   },
   "outputs": [],
   "source": [
    "# Conduct resolution on two CNF clauses.\n",
    "def resolve(arg_one, arg_two):\n",
    "    resolved = False\n",
    "\n",
    "    s1 = make_sentence(arg_one)\n",
    "    s2 = make_sentence(arg_two)\n",
    "\n",
    "    resolve_s1 = None\n",
    "    resolve_s2 = None\n",
    "\n",
    "    # Two for loops that iterate through the two clauses.\n",
    "    for i in s1:\n",
    "        if isNotList(i):\n",
    "            a1 = i[1]\n",
    "            a1_not = True\n",
    "        else:\n",
    "            a1 = i\n",
    "            a1_not = False\n",
    "\n",
    "        for j in s2:\n",
    "            if isNotList(j):\n",
    "                a2 = j[1]\n",
    "                a2_not = True\n",
    "            else:\n",
    "                a2 = j\n",
    "                a2_not = False\n",
    "\n",
    "            # cancel out two literals such as 'a' $ ['not', 'a']\n",
    "            if a1 == a2:\n",
    "                if a1_not != a2_not:\n",
    "                    # Return False if resolution already happend\n",
    "                    # but contradiction still exists.\n",
    "                    if resolved:\n",
    "                        return False\n",
    "                    else:\n",
    "                        resolved = True\n",
    "                        resolve_s1 = i\n",
    "                        resolve_s2 = j\n",
    "                        break\n",
    "                    # Return False if not resolution happened\n",
    "    if not resolved:\n",
    "        return False\n",
    "\n",
    "    # Remove the literals that are canceled\n",
    "    s1.remove(resolve_s1)\n",
    "    s2.remove(resolve_s2)\n",
    "\n",
    "    # # Remove duplicates\n",
    "    result = clear_duplicate(s1 + s2)\n",
    "\n",
    "    # Format the result.\n",
    "    if len(result) == 1:\n",
    "        return result[0]\n",
    "    elif len(result) > 1:\n",
    "        result.insert(0, 'or')\n",
    "\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "id": "hdUr8fmydy7S"
   },
   "outputs": [],
   "source": [
    "# Prepare sentences for resolution.\n",
    "def make_sentence(arg):\n",
    "    if isLiteral(arg) or isNotList(arg):\n",
    "        return [arg]\n",
    "    if isOrList(arg):\n",
    "        return clear_duplicate(arg[1:])\n",
    "    return\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "id": "NekMOCt7dy7S"
   },
   "outputs": [],
   "source": [
    "# Clear out duplicates in a sentence.\n",
    "def clear_duplicate(arg):\n",
    "    result = []\n",
    "    for i in range(0, len(arg)):\n",
    "        if arg[i] not in arg[i+1:]:\n",
    "            result.append(arg[i])\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "id": "hV8EoGCmdy7S"
   },
   "outputs": [],
   "source": [
    "# Check whether a sentence is a legal CNF clause.\n",
    "def isClause(sentence):\n",
    "    if isLiteral(sentence):\n",
    "        return True\n",
    "    if isNotList(sentence):\n",
    "        if isLiteral(sentence[1]):\n",
    "            return True\n",
    "        else:\n",
    "            return False\n",
    "    if isOrList(sentence):\n",
    "        for i in range(1, len(sentence)):\n",
    "            if len(sentence[i]) > 2:\n",
    "                return False\n",
    "            elif not isClause(sentence[i]):\n",
    "                return False\n",
    "        return True\n",
    "    return False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {
    "id": "Zo1W60jZdy7S"
   },
   "outputs": [],
   "source": [
    "# Check if a sentence is a legal CNF.\n",
    "def isCNF(sentence):\n",
    "    if isClause(sentence):\n",
    "        return True\n",
    "    elif isAndList(sentence):\n",
    "        for s in sentence[1:]:\n",
    "            if not isClause(s):\n",
    "                return False\n",
    "        return True\n",
    "    return False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {
    "id": "srmoW5GKdy7S"
   },
   "outputs": [],
   "source": [
    "# Negate a sentence.\n",
    "def negation(sentence):\n",
    "    if isLiteral(sentence):\n",
    "        return ['not', sentence]\n",
    "    if isNotList(sentence):\n",
    "        return sentence[1]\n",
    "\n",
    "    # DeMorgan:\n",
    "    if isAndList(sentence):\n",
    "        result = ['or']\n",
    "        for i in sentence[1:]:\n",
    "            if isNotList(sentence):\n",
    "                result.append(i[1])\n",
    "            else:\n",
    "                result.append(['not', sentence])\n",
    "        return result\n",
    "    if isOrList(sentence):\n",
    "        result = ['and']\n",
    "        for i in sentence[:]:\n",
    "            if isNotList(sentence):\n",
    "                result.append(i[1])\n",
    "            else:\n",
    "                result.append(['not', i])\n",
    "        return result\n",
    "    return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {
    "id": "JxmO2gvndy7S"
   },
   "outputs": [],
   "source": [
    "# Convert a sentence into CNF.\n",
    "def convertCNF(sentence):\n",
    "    while not isCNF(sentence):\n",
    "        if sentence is None:\n",
    "            return None\n",
    "        sentence = makeCNF(sentence)\n",
    "    return sentence"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {
    "id": "dJQMBb-Edy7S"
   },
   "outputs": [],
   "source": [
    "# Help make a sentence into CNF.\n",
    "def makeCNF(sentence):\n",
    "    if isLiteral(sentence):\n",
    "        return sentence\n",
    "\n",
    "    if (type(sentence).__name__ == 'list'):\n",
    "        operand = sentence[0]\n",
    "        if isNotList(sentence):\n",
    "            if isLiteral(sentence[1]):\n",
    "                return sentence\n",
    "            cnf = makeCNF(sentence[1])\n",
    "            if cnf[0] == 'not':\n",
    "                return makeCNF(cnf[1])\n",
    "            if cnf[0] == 'or':\n",
    "                result = ['and']\n",
    "                for i in range(1, len(cnf)):\n",
    "                    result.append(makeCNF(['not', cnf[i]]))\n",
    "                return result\n",
    "            if cnf[0] == 'and':\n",
    "                result = ['or']\n",
    "                for i in range(1, len(cnf)):\n",
    "                    result.append(makeCNF(['not', cnf[i]]))\n",
    "                return result\n",
    "            return \"False: not\"\n",
    "\n",
    "        # Implication Elimination:\n",
    "        if operand == 'implies' and len(sentence) == 3:\n",
    "            return makeCNF(['or', ['not', makeCNF(sentence[1])], makeCNF(sentence[2])])\n",
    "            # Biconditional Elimination:\n",
    "        if operand == 'biconditional' and len(sentence) == 3:\n",
    "            s1 = makeCNF(['implies', sentence[1], sentence[2]])\n",
    "            s2 = makeCNF(['implies', sentence[2], sentence[1]])\n",
    "            return makeCNF(['and', s1, s2])\n",
    "\n",
    "        if isAndList(sentence):\n",
    "            result = ['and']\n",
    "            for i in range(1, len(sentence)):\n",
    "                cnf = makeCNF(sentence[i])\n",
    "                # Distributivity:\n",
    "                if isAndList(cnf):\n",
    "                    for i in range(1, len(cnf)):\n",
    "                        result.append(makeCNF(cnf[i]))\n",
    "                    continue\n",
    "                result.append(makeCNF(cnf))\n",
    "            return result\n",
    "\n",
    "        if isOrList(sentence):\n",
    "            result1 = ['or']\n",
    "            for i in range(1, len(sentence)):\n",
    "                cnf = makeCNF(sentence[i])\n",
    "                # Distributivity:\n",
    "                if isOrList(cnf):\n",
    "                    for i in range(1, len(cnf)):\n",
    "                        result1.append(makeCNF(cnf[i]))\n",
    "                    continue\n",
    "                result1.append(makeCNF(cnf))\n",
    "                # Associativity:\n",
    "            while True:\n",
    "                result2 = ['and']\n",
    "                and_clause = None\n",
    "                for r in result1:\n",
    "                    if isAndList(r):\n",
    "                        and_clause = r\n",
    "                        break\n",
    "\n",
    "                # Finish when there's no more 'and' lists\n",
    "                # inside of 'or' lists\n",
    "                if not and_clause:\n",
    "                    return result1\n",
    "\n",
    "                result1.remove(and_clause)\n",
    "\n",
    "                for i in range(1, len(and_clause)):\n",
    "                    temp = ['or', and_clause[i]]\n",
    "                    for o in result1[1:]:\n",
    "                        temp.append(makeCNF(o))\n",
    "                    result2.append(makeCNF(temp))\n",
    "                result1 = makeCNF(result2)\n",
    "            return None\n",
    "    return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {
    "id": "A9-GG3kZdy7S"
   },
   "outputs": [],
   "source": [
    "# Below are 4 functions that check the type of a variable\n",
    "def isLiteral(item):\n",
    "    if type(item).__name__ == 'str':\n",
    "        return True\n",
    "    return False\n",
    "\n",
    "\n",
    "def isNotList(item):\n",
    "    if type(item).__name__ == 'list':\n",
    "        if len(item) == 2:\n",
    "            if item[0] == 'not':\n",
    "                return True\n",
    "    return False\n",
    "\n",
    "\n",
    "def isAndList(item):\n",
    "    if type(item).__name__ == 'list':\n",
    "        if len(item) > 2:\n",
    "            if item[0] == 'and':\n",
    "                return True\n",
    "    return False\n",
    "\n",
    "\n",
    "def isOrList(item):\n",
    "    if type(item).__name__ == 'list':\n",
    "        if len(item) > 2:\n",
    "            if item[0] == 'or':\n",
    "                return True\n",
    "    return False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {
    "id": "WtTw8S6Jdy7T"
   },
   "outputs": [],
   "source": [
    "\n",
    "CLEAR()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "t7JsjBnvdy7T",
    "outputId": "cb77af5f-5896-4ee2-ae28-249292d4bfa9"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 34,
     "metadata": {
      "tags": []
     },
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Test1\n",
    "TELL(['implies', 'p', 'q'])\n",
    "TELL(['implies', 'r', 's'])\n",
    "ASK(['implies',['or','p','r'], ['or', 'q', 's']])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {
    "id": "Jwx0DdvVdy7U"
   },
   "outputs": [],
   "source": [
    "CLEAR()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "5fY68bCPdy7U",
    "outputId": "7910b6a6-38b8-4588-9523-12edb00340a0"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 36,
     "metadata": {
      "tags": []
     },
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Test2\n",
    "TELL('p')\n",
    "TELL(['implies',['and','p','q'],'r'])\n",
    "TELL(['implies',['or','s','t'],'q'])\n",
    "TELL('t')\n",
    "ASK('r')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {
    "id": "ZfaiP3pedy7U"
   },
   "outputs": [],
   "source": [
    "CLEAR()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "MRIYXwmWdy7U",
    "outputId": "e4df7d6a-8727-4c93-ee1c-701bb283138e"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 38,
     "metadata": {
      "tags": []
     },
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Test3\n",
    "TELL('a')\n",
    "TELL('b')\n",
    "TELL('c')\n",
    "TELL('d')\n",
    "ASK(['or', 'a', 'b', 'c', 'd'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {
    "id": "2Ce_0aqAdy7U"
   },
   "outputs": [],
   "source": [
    "CLEAR()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "XRKPkAbGdy7U",
    "outputId": "49ccedcc-36f4-41b4-f12a-d005640b8012"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 40,
     "metadata": {
      "tags": []
     },
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Test4\n",
    "TELL('a')\n",
    "TELL('b')\n",
    "TELL(['or', ['not', 'a'], 'b'])\n",
    "TELL(['or', 'c', 'd'])\n",
    "TELL('d')\n",
    "ASK('c')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {
    "id": "qgtkt4Dldy7U"
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "name": "resolution.ipynb",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}