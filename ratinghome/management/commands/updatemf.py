from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from destination.models import Mf_result, Places, Place_rating 


class Command(BaseCommand):
    help= 'command to update matrix factorization table'
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        Mf_result.objects.all().delete()
        place=Places.objects.all()
        x=['user_id']
        MF=[]
        for obj in place:
            x.append(obj.id)
            MF.append(obj.id)

        df=pd.DataFrame(columns=x)

        


        rating=Place_rating.objects.all()

        y=[]
        for i in rating:
            y.append(i.user.id)

        y=set(y)

        

        y=list(y)

        

        df['user_id']=y



        df.set_index('user_id',inplace=True)

        my_dct=[]
        for obj in Place_rating.objects.all().values():
            obj.pop('id')
            my_dct.append(obj)
            



        for index in range(len(my_dct)):
                dictionary=my_dct[index]
                rate_place_user_list=list(dictionary.values())
                df.at[rate_place_user_list[2],rate_place_user_list[1]]=rate_place_user_list[0]
                



        


        df = df.fillna(0)



        matrixcopy=df.copy()



        user_place_matrix=matrixcopy.to_numpy()

    

        

        class MatrixFactorization():
            def __init__(self, R, K, alpha, beta, iterations):
                """
                Perform matrix factorization to predict empty
                entries in a matrix.

                Arguments
                - R (ndarray)   : user-place rating matrix
                - K (int)       : number of latent features
                - alpha (float) : learning rate :in most of case we consider alpha=0.0002
                - beta (float)  : regularization parameter beta=0.02 regularization is done to minimize overfitting
                """

                self.R = R
                self.num_users, self.num_places = R.shape
                self.K = K
                self.alpha = alpha
                self.beta = beta
                self.iterations = iterations

            def trainingmatrix(self):
                # Initialize user and places latent feature matrix
                self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
                self.Q = np.random.normal(scale=1./self.K, size=(self.num_places, self.K))

                # Initialize the biases
                self.b_u = np.zeros(self.num_users)
                self.b_i = np.zeros(self.num_places)
                self.b = np.mean(self.R[np.where(self.R != 0)])

                # Create a list of training samples
                self.samples = [
                    (i, j, self.R[i, j])
                    for i in range(self.num_users)
                    for j in range(self.num_places)
                    if self.R[i, j] > 0
                ]

                # Perform stochastic gradient descent for number of iterations
                training_process = []
                for i in range(self.iterations):
                    np.random.shuffle(self.samples)
                    self.stochasticGD()
                    mse = self.meansquareerror()
                    training_process.append((i, mse))
                    if (i+1) % 10 == 0:
                        print("Iteration: %d ; error = %.4f" % (i+1, mse))

                return training_process

            def meansquareerror(self):
                """
                A function to compute the total mean square error
                """
                xs, ys = self.R.nonzero()
                predicted = self.full_matrix()
                error = 0
                for x, y in zip(xs, ys):
                    error += pow(self.R[x, y] - predicted[x, y], 2)
                return np.sqrt(error)

            def stochasticGD(self):
                """
                Perform stochastic graident descent
                """
                for i, j, r in self.samples:
                    # Computer prediction and error
                    prediction = self.get_rating(i, j)
                    e = (r - prediction)

                    # Update biases
                    self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
                    self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])

                    # Update user and places latent feature matrices
                    self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
                    self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])

            def get_rating(self, i, j):
                """
                Get the predicted rating of user i and places j
                """
                prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
                return prediction

            def full_matrix(self):
                """
                Computer the full matrix using the resultant biases, P and Q
                """
                return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)

        mf = MatrixFactorization(user_place_matrix, K=7, alpha=0.01, beta=0.02, iterations=5000)

        mf.trainingmatrix()

        data=mf.full_matrix()

        

        rate_place_user_matrix=pd.DataFrame(data,columns=MF)

        


        idx=0
        new_column=y
        rate_place_user_matrix.insert(loc=idx,column='user_id',value=new_column)
        rate_place_user_matrix.set_index('user_id',inplace=True)
        our_dct=[]
        for index,row in rate_place_user_matrix.iterrows():
            for col in rate_place_user_matrix:
                obj= {'rate': row[col], 'place_id' : col, 'user_id': index}
                our_dct.append(obj)
        for i in our_dct:
            m = Mf_result(**i)
            m.save()

        



    
        
