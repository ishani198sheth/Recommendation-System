
import math
import sys
from collections import OrderedDict


file = open(sys.argv[1])
user1 = str(sys.argv[2])
movie1 = str(sys.argv[3])
k = int(sys.argv[4])

def pearson_correlation(movies, users, minimum_similarity, rating_matrix):
    # The function returns a similarity matrix which is a matrix that has calculated values for similarity between all the users.
    # Initially all values are assigned to minimum similarity

    similarity_matrix = [[minimum_similarity for i in range(len(users))] for j in range(len(users))]
   
       
    for i in range(len(users)):
        for j in range(i):
            if i!=j:
                # Getting all the common movies rated between user i and user j
                common_movies = []
                user1=[]
                otheruser=[]
                ratings_i = rating_matrix[i]        # the i(user) th row has all the ratings by user i
                ratings_j = rating_matrix[j]        # the j(user) th row has aall the ratings by user j
                for l in range(len(movies)):
                    if ratings_i[l]!=invalid_rating:
                        user1.append(l)
                    if ratings_j[l]!=invalid_rating:
                        otheruser.append(l)
                    if ratings_i[l]!=invalid_rating and ratings_j[l]!=invalid_rating:
                        common_movies.append(l)

                if len(common_movies)>1:
                    numerator = 0
                    denominator_i = 0
                    denominator_j = 0
                    avg_i = 0
                    avg_j = 0

                    # Calculate the average rating for user_i and user_j
                    
                    for user_i in user1:
                        avg_i += ratings_i[user_i]
                    avg_i = avg_i/len(user1)
                    for user_j in otheruser:    
                        avg_j += ratings_j[user_j]
                    avg_j = avg_j/len(otheruser)

                    # computing summations for users who have rated common movies
                    for movie in common_movies:
                        numerator += (ratings_i[movie] - avg_i) * (ratings_j[movie] - avg_j)
                        denominator_i += (ratings_i[movie] - avg_i)**2
                        denominator_j += (ratings_j[movie] - avg_j)**2
                    denominator = math.sqrt(denominator_i) * math.sqrt(denominator_j)

                    # If denominator is not equal to 0 calculate numerator/denominator
                    if denominator!=0:
                        similarity_matrix[i][j] = numerator/denominator
                    else:
                        similarity_matrix[i][j] = 0

    # forming the complete matrix
    for i in range(len(users)):
        for j in range(len(users)):
            if j>i:
                similarity_matrix[i][j] = similarity_matrix[j][i]

    
    return similarity_matrix


def k_nearest_neighbors(similaritymatrix,user,userlist,k):
    neighbors={}
    #finds the k nearest neighbors for the given user and sorts them in descending order of value and ascending order of key
    for eachuser1 in userlist:
        neighbors[eachuser1]=similarity_matrix[users.index(user)][users.index(eachuser1)]
    #ordered= [v[0] for v in sorted(neighbors.iteritems(), key=lambda(k, v): (-v, k))]
    ordered=[v[0] for v in sorted(neighbors.items(), key=lambda(k,v): (v,k), reverse=True)] 
    topk=ordered[0:k]
    # add the logic for sorting the elements based on user id in case of tie
    for element in topk:
            
        print element+" "+str(similarity_matrix[userlist.index(user)][userlist.index(element)])
    
    return topk


def predict(movies, users, rating_matrix, similarity_matrix, invalid_rating, user1,prediction_movie,k,top):

    # get the movies that the given user has rated and the one it has not rated.
    user_rated_movies = []
    user_unrated_movies = []
    
    #initializing the avg for given user and the other users
    avg_user1 =0
    avg_user=0
    
    
    similarity_list=[]
    
    
    # users who have rated movie to be predicted
    for user2 in users:
        if rating_matrix[users.index(user2)][movies.index(prediction_movie)] !=invalid_rating:
            user_rated_movies.append(user2)
            #print user2 +" "+str(rating_matrix[users.index(user2)][movies.index(movie1)])
        else:
            user_unrated_movies.append(user2)
            
   # average for user1
    movielist=[]   
    for movie2 in movies:
        if rating_matrix[users.index(user1)][movies.index(movie2)] !=invalid_rating:
            avg_user1 += rating_matrix[users.index(user1)][movies.index(movie2)]      
            movielist.append(rating_matrix[users.index(user1)][movies.index(movie2)])
    avg_user1 = avg_user1/len(movielist)
    #print(avg_user1)     
    
    # average list for all other users
      
    numerator = 0
    denominator = 0
        #count = 0
    #print user_rated_movies
    
    # based on k-nearest neighbor it will find the list of similar users
    for eachuser1 in user_rated_movies:
        if eachuser1 in top:
            similarity_list.append(eachuser1)
    #ordered= list(OrderedDict(sorted(similarity_dict.items(), key=lambda t: t[1], reverse=True)))
    
    #similarity_list=ordered[0:4]    
    #print similarity_list
    
    #for the users in similarity list it will predict the prediction value for the movie for given user
    
    for eachuser in similarity_list:
        movielist=[]   
        for movie2 in movies:
            if rating_matrix[users.index(eachuser)][movies.index(movie2)] !=invalid_rating:
                avg_user += rating_matrix[users.index(eachuser)][movies.index(movie2)]      
                movielist.append(rating_matrix[users.index(eachuser)][movies.index(movie2)])
        avg_user = avg_user/len(movielist)
        
        
     
        numerator += (rating_matrix[users.index(eachuser)][movies.index(prediction_movie)])*similarity_matrix[users.index(user1)][users.index(eachuser)]
        denominator += abs(similarity_matrix[users.index(user1)][users.index(eachuser)])
       
    if denominator != 0:
        
        predicted_rating=(numerator/denominator)
    else:
        predicted_rating=0
    #print(predicted_ratings)
    return predicted_rating


    
def ratings_range(start, stop, step):
    ratings_list = []
    i = start
    while i<=stop:
        ratings_list.append(i)
        i+=step
    return ratings_list    
    
if k>0:
    movies = []
    users = []
    ratings = []
    minimum_rating = 0.5
    maximum_rating = 5
    step_rating = 0.5
    invalid_rating = -1
    minimum_similarity = 0
    valid_ratings = ratings_range(minimum_rating, maximum_rating, step_rating) 
    
                                  
    for line in file:
        data = line.strip().split('\t')
        if len(data) != 3:
            print('The length of data '+str(len(data))+' is not a valid length. It should be 3.')
        else:
            if float(data[1]) in valid_ratings:
                ratings.append(data)
                if data[2] not in movies:
                    movies.append(data[2])
                if data[0] not in users:
                    users.append(data[0])
            else:
                print('The rating '+str(data[1])+ ' is not a valid rating.It should be in range of 0.5 to 5')
    
        
        # if there exists any movies and users with valid ratings then it will move ahead
        
    if len(movies)>0 and len(users)>0:

            # Construct a rating matrix where rows correspond to movies and columns correspond to users.
            # The entries in the matrix are corresponding ratings of the user for that movie
            
        rating_matrix = [[invalid_rating for i in range(len(movies))] for j in range(len(users))]
        for data in ratings:
            rating_matrix[users.index(data[0])][movies.index(data[2])] = float(data[1])
        #print movies
            
            # After getting the rating matrix we calculate the similarity matrix(pearson correlation matrix) between all of the users
            # The similarity matrix is nothing but similarity between each user: users are rows and users are column.
            # The entries in the matrix are the similarity between those users.
        
        if user1 in users:
            similarity_matrix = pearson_correlation(movies, users, minimum_similarity, rating_matrix)
            
            # After getting the similarity matrix I get the top_k users i.e. k-nearest neighbors of given user in descending order.
            top=k_nearest_neighbors(similarity_matrix,user1,users,k)
        else:
            print ('The user does not exist in the list')            
            # If the user1(the one given as input in argument) exists in the list of users who have rated the movie
            # Then it will find the prediction for that user for the movie1(the movie given in argument)
        if user1 in users:
            if movie1 in movies:
                predicted_rating = predict(movies, users, rating_matrix, similarity_matrix, invalid_rating, user1, movie1,k,top)
                print
                print predicted_rating
            else:
                print(movie1+' not in list')
        else:
            print('The user has no predicted movies')
    else:
        print('The file has no movie or user. It is empty.')
else:
    print('k<=0 is not possible.')