
import math
import sys
from collections import OrderedDict

def ratings_range(start, stop, step):
    output = []
    i = start
    while i<=stop:
        output.append(i)
        i+=step
    return output

def predict(movies, users, rating_matrix, similarity_matrix, invalid_rating, user1,prediction_movie,k,top):

    # Fetching the ratings given by user mentioned.
    user_rated_movies = []
    user_unrated_movies = []
    #predicted_ratings = []
    avg_user1 =0
    avg_user=0
    
    similarity_list=[]
    #similarity_dict={}
    #avg_list=[]
    #for movie_ratings in rating_matrix:
    #    user_ratings.append(movie_ratings[movies.index(prediction_movie)])
    
    
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
      
    #for user in user_rated_movies:
    #    movielist=[]   
    #    for movie2 in movies:
    #        if rating_matrix[users.index(user)][movies.index(movie2)] !=invalid_rating:
    #            avg_user1 += rating_matrix[users.index(user)][movies.index(movie2)]      
    #            movielist.append(rating_matrix[users.index(user)][movies.index(movie2)])
    #    avg_user = avg_user/len(movielist)
    #    avg_list.append(avg_user)  
      
        # In case the neighborhood is smaller than or equal to the number of unrated movies, we consider the neighborhood.
        # Else, we consider all unrated movies as they all fall under neighborhood
        # Calculating predicted rating using top n movies rated by user
    numerator = 0
    denominator = 0
        #count = 0
    #print user_rated_movies
    
    for eachuser1 in user_rated_movies:
        if eachuser1 in top:
            similarity_list.append(eachuser1)
    #ordered= list(OrderedDict(sorted(similarity_dict.items(), key=lambda t: t[1], reverse=True)))
    
    #similarity_list=ordered[0:4]    
    #print similarity_list
    for eachuser in similarity_list:
        movielist=[]   
        for movie2 in movies:
            if rating_matrix[users.index(eachuser)][movies.index(movie2)] !=invalid_rating:
                avg_user += rating_matrix[users.index(eachuser)][movies.index(movie2)]      
                movielist.append(rating_matrix[users.index(eachuser)][movies.index(movie2)])
        avg_user = avg_user/len(movielist)
        
        
        #similarity_list.append(similarity_matrix[users.index(user1)][users.index(eachuser)])
        #similarity_list.sort(reverse=True)
        #similarity_list = heapq._nlargest(k,similarity_list)
        numerator += (rating_matrix[users.index(eachuser)][movies.index(prediction_movie)])*similarity_matrix[users.index(user1)][users.index(eachuser)]
        denominator += abs(similarity_matrix[users.index(user1)][users.index(eachuser)])
        
        #for w in weights:
        #    if count<n:
        #        numerator += user_ratings[movies.index(w[0])] * w[1]
        #        denominator += abs(w[1])
        #        count += 1
        #    else:
        #        break
    if denominator != 0:
        
        predicted_ratings=(numerator/denominator)
    #print(predicted_ratings)
    return predicted_ratings

def k_nearest_neighbors(similaritymatrix,user,userlist,k):
    neighbors={}
   
    for eachuser1 in userlist:
        neighbors[eachuser1]=similarity_matrix[users.index(user)][users.index(eachuser1)]
    ordered= list(OrderedDict(sorted(neighbors.items(), key=lambda t: t[1], reverse=True)))
    
    topk=ordered[0:k]
    for element in topk:
            
        print element+" "+str(similarity_matrix[userlist.index(user)][userlist.index(element)])
    
    return topk

def pearson_correlation(movies, users, min_similarity, rating_matrix):
    # This matrix stores similarity for item corresponding to row and item corresponding to column.
    # The diagonal elements therefore should ideally be 1. They are however kept at minimum_similarity for ease of computation
    # The similarity matrix calculated below is lower triangular at first. The values are then duplicated for the upper half
    similarity_matrix = [[min_similarity for i in range(len(users))] for j in range(len(users))]
   
       
    for i in range(len(users)):
        for j in range(i):
            if i!=j:
                # Finding common users for movies i and j
                common_movies = []
                user1=[]
                otheruser=[]
                ratings_i = rating_matrix[i]        # the i(user) th row has all ratings for this movie
                ratings_j = rating_matrix[j]        # the j(movie) th row has all ratings for this movie
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

                    # Calculating average ratings for both movies corresponding to common users
                    
                    for movie in user1:
                        avg_i += ratings_i[movie]
                    avg_i = avg_i/len(user1)
                    for movie in otheruser:    
                        avg_j += ratings_j[movie]
                    avg_j = avg_j/len(otheruser)

                    # calculating numerator and denominator summations for the common users
                    for movie in common_movies:
                        numerator += (ratings_i[movie] - avg_i) * (ratings_j[movie] - avg_j)
                        denominator_i += (ratings_i[movie] - avg_i)**2
                        denominator_j += (ratings_j[movie] - avg_j)**2
                    denominator = math.sqrt(denominator_i) * math.sqrt(denominator_j)

                    # Checking if denominator is valid
                    if denominator!=0:
                        similarity_matrix[i][j] = numerator/denominator

    # Duplicating values for the upper half
    for i in range(len(users)):
        for j in range(len(users)):
            if j>i:
                similarity_matrix[i][j] = similarity_matrix[j][i]

    
    return similarity_matrix

if __name__ == '__main__':
    file = open(sys.argv[1])
    user1 = str(sys.argv[2])
    movie1 = str(sys.argv[3])
    k = int(sys.argv[4])

    if k>0:
        movies = []
        users = []
        ratings = []
        min_rating = 0.5
        max_rating = 5
        step_rating = 0.5
        invalid_rating = -1
        min_similarity = 0
        valid_ratings = ratings_range(min_rating, max_rating, step_rating)                
        for line in file:
            data = line.strip().split('\t')
            if len(data) != 3:
                print('Incorrect input line. Skipping it.')
            else:
                if float(data[1]) in valid_ratings:
                    ratings.append(data)
                    if data[2] not in movies:
                        movies.append(data[2])
                    if data[0] not in users:
                        users.append(data[0])
                else:
                    print('Rating is not valid. Skipping the record.')
        if len(movies)>0 and len(users)>0:

            # Constructing a matrix in which rows correspond to users and columns correspond to movies.
            # The entries are corresponding ratings
            rating_matrix = [[invalid_rating for i in range(len(movies))] for j in range(len(users))]
            for data in ratings:
                rating_matrix[users.index(data[0])][movies.index(data[2])] = float(data[1])
            #print movies
            
            similarity_matrix = pearson_correlation(movies, users, min_similarity, rating_matrix)
            top=k_nearest_neighbors(similarity_matrix,user1,users,k)
            

            if user1 in users:

                predicted_ratings = predict(movies, users, rating_matrix, similarity_matrix, invalid_rating, user1, movie1,k,top)
                print
                print predicted_ratings
                
                
       #         if len(predicted_ratings)>0:
       #             predicted_ratings.sort(key=lambda tup: (-tup[1], tup[0]))
       #             print('Recommended Items are :')
       #             count = 0
       #             for p in predicted_ratings:
       #                 if count<k:
       #                     print(p[0],p[1])
			    #
       #                     count+=1

            else:
                print('Given user\'s rating data is not provided')
        else:
            print('Incorrect input file.')
    else:
        print('Invalid input. Neighborhood and number of movies to be recommended should be greater than 0.')
