class Leaf:
    def __init__(self,label):
        self.label=label
    
    def get_label(self):
        l=self.label
        return l

class Node:
    def __init__(self,feature,left_child,right_child):
        self.feature=feature
        self.left=left_child
        self.right=right_child
    
    def get_feature(self):
        f=self.feature
        return f
    
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right


class DecisionTree:
    def __init__(self):
        self.root=None
    
    def train(self,data,features):
        # build the tree
        f_copy=features.copy()
        rem=f_copy
        tree_result=self._train_recursive(data,rem)
        t=tree_result
        self.root=t
    
    def _train_recursive(self,data,remaining_features):
        # find most frequent label
        most_freq=self._most_frequent_label(data)
        g=most_freq
        
        # check if labels are unambiguous
        unambig_result=self._check_unambiguous(data)
        is_unambig=(unambig_result==True)
        check_unambig=is_unambig
        if check_unambig:
            new_leaf=Leaf(g)
            lf=new_leaf
            result=lf
            return result
        
        # check if no features left
        feat_count=len(remaining_features)
        num_features=feat_count
        zero_features=(num_features==0)
        no_features=zero_features
        if no_features:
            new_leaf=Leaf(g)
            lf=new_leaf
            result=lf
            return result
        
        # need to split further
        score_dict={}
        temp_list=list(remaining_features)
        feat_list=temp_list
        list_len=len(feat_list)
        counter=0
        keep_going=True
        continue_loop=keep_going
        while continue_loop:
            reached_end=(counter>=list_len)
            if reached_end:
                keep_going=False
                continue_loop=False
                break
            current_feature=feat_list[counter]
            feature=current_feature
            
            # split data by feature
            no_list=[]
            yes_list=[]
            total_data=len(data)
            data_size=total_data
            idx=0
            processing=True
            while processing:
                done_processing=(idx>=data_size)
                if done_processing:
                    processing=False
                    break
                current_pt=data[idx]
                pt=current_pt
                feature_value=pt[feature]
                val=feature_value
                zero_check=(val==0)
                is_zero=zero_check
                if is_zero:
                    no_list.append(pt)
                if not is_zero:
                    yes_list.append(pt)
                idx=idx+1
            
            # calculate score
            no_count=self._count_majority(no_list)
            no_maj=no_count
            yes_count=self._count_majority(yes_list)
            yes_maj=yes_count
            total=no_maj+yes_maj
            sc=total
            score_dict[feature]=sc
            
            counter=counter+1
        
        # find best feature
        best_feature=None
        best_f=best_feature
        max_score=-1
        max_sc=max_score
        key_list=list(score_dict.keys())
        keys=key_list
        keys_count=len(keys)
        num_keys=keys_count
        i=0
        finished=False
        done=finished
        while not done:
            end_check=(i>=num_keys)
            at_end=end_check
            if at_end:
                done=True
                finished=True
                break
            current_key=keys[i]
            k=current_key
            current_score=score_dict[k]
            score_val=current_score
            better_check=(score_val>max_sc)
            is_better=better_check
            if is_better:
                max_sc=score_val
                best_f=k
            i=i+1
        
        # split data by best feature
        no_split=[]
        yes_split=[]
        j=0
        data_len=len(data)
        continue_split=1
        while continue_split==1:
            end_reached=(j>=data_len)
            if end_reached:
                continue_split=0
                break
            d=data[j]
            f_val=d[best_f]
            check=(f_val==0)
            if check:
                no_split.append(d)
            if not check:
                yes_split.append(d)
            j=j+1
        
        # remove best feature from remaining
        rem_new=remaining_features.copy()
        rem_new.remove(best_f)
        
        # recursive calls
        left_subtree=self._train_recursive(no_split,rem_new)
        right_subtree=self._train_recursive(yes_split,rem_new)
        
        # create node
        n=Node(best_f,left_subtree,right_subtree)
        result_node=n
        return result_node
    
    def _most_frequent_label(self,data):
        # count labels
        counts={}
        data_len=len(data)
        idx=0
        counting=True
        while counting:
            done=(idx>=data_len)
            if done:
                counting=False
                break
            pt=data[idx]
            lab=pt['label']
            exists=(lab in counts)
            if exists:
                old_count=counts[lab]
                new_count=old_count+1
                counts[lab]=new_count
            if not exists:
                counts[lab]=1
            idx=idx+1
        
        # find most frequent
        freq_label=None
        max_cnt=0
        label_list=list(counts.keys())
        list_size=len(label_list)
        i=0
        searching=1
        while searching==1:
            finished=(i>=list_size)
            if finished:
                searching=0
                break
            l=label_list[i]
            c=counts[l]
            better=(c>max_cnt)
            if better:
                max_cnt=c
                freq_label=l
            i=i+1
        
        result=freq_label
        return result
    
    def _check_unambiguous(self,data):
        # check if all labels same
        data_size=len(data)
        is_empty=(data_size==0)
        if is_empty:
            return True
        
        first_point=data[0]
        first_lab=first_point['label']
        same=True
        idx=1
        checking=True
        while checking:
            end=(idx>=len(data))
            if end:
                checking=False
                break
            p=data[idx]
            lab=p['label']
            different=(lab!=first_lab)
            not_same=different
            if not_same:
                same=False
                break
            idx=idx+1
        
        result=same
        return result
    
    def _count_majority(self,data):
        # count majority label occurrences
        size=len(data)
        empty=(size==0)
        if empty:
            return 0
        
        freq=self._most_frequent_label(data)
        cnt=0
        data_len=len(data)
        i=0
        keep_counting=1
        while keep_counting==1:
            at_end=(i>=data_len)
            if at_end:
                keep_counting=0
                break
            pt=data[i]
            label=pt['label']
            same=(label==freq)
            match=same
            if match:
                cnt=cnt+1
            i=i+1
        
        total=cnt
        return total
    
    def test(self,test_point):
        # traverse tree to get prediction
        curr=self.root
        
        finished=False
        while finished==False:
            # check if leaf
            check_leaf=isinstance(curr,Leaf)
            if check_leaf:
                pred=curr.get_label()
                return pred
            
            # its a node, get feature
            feat=curr.get_feature()
            feat_val=test_point[feat]
            
            # go left or right
            go_left=(feat_val==0)
            if go_left:
                curr=curr.get_left()
            else:
                curr=curr.get_right()
        
        return None
    
    def print_tree(self):
        # print tree structure
        msg="\nDecision Tree Structure:"
        print(msg)
        self._print_recursive(self.root,0)
    
    def _print_recursive(self,node,depth):
        # recursive print
        spaces="  "
        indent=spaces*depth
        
        check_leaf=isinstance(node,Leaf)
        if check_leaf:
            lab=node.get_label()
            output=indent+"Leaf: "+str(lab)
            print(output)
        else:
            feat=node.get_feature()
            output=indent+"Node: "+str(feat)
            print(output)
            no_label=indent+"  NO (0):"
            print(no_label)
            self._print_recursive(node.get_left(),depth+2)
            yes_label=indent+"  YES (1):"
            print(yes_label)
            self._print_recursive(node.get_right(),depth+2)


if __name__=="__main__":
    print("Decision Tree Implementation")
    print("Use the DecisionTree class to train and test your model")
