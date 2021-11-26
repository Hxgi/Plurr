from ..models.inboxModel import Inbox
from ..models.authorModel import Author
from ..serializers import InboxSerializer, AuthorSerializer, LikeSerializer, PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..utils import getPageNumber, getPageSize, getPaginatedObject, loggedInUserIsAuthor, getLoggedInAuthorObject


def postIsInInbox(post, inbox):
  try:
    for item in inbox.items:
      if (item.type == "post" and item.id == post.id):
        return True
    return False
  except:
    return False

def followIsInInbox(follow, inbox):
  try:
    for item in inbox.items:
      if (
        item.get("type", None) == "follow" 
        and item.actor.id == follow.actor.id 
        and item.object.id == follow.object.id
      ):
        return True
    return False
  except:
    return False

def likeIsInInbox(like, inbox):
  try:
    for item in inbox.items:
      if (
        item.type == "like" 
        and item.author.id == like.author.id 
        and item.object == like.object
      ):
        return True
    return False
  except:
    return False

@api_view(['POST', 'GET', 'DELETE'])
def InboxList(request, author_uuid):
  try:  # try to get the specific author and post
      authorObject = Author.objects.get(uuid=author_uuid)
  except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)

  # Create a new comment
  if request.method == 'POST':
    try:  # try to get the inbox
        inbox = Inbox.objects.get(author=authorObject.id)
    except:  # create an inbox if one doesn't already exist
        serializer = InboxSerializer(data={'author': authorObject.id})
        if serializer.is_valid():
          serializer.save(author=author_uuid)
        inbox = Inbox.objects.get(author=authorObject.id)

    try:  # try to get the item type
        item_type = request.data['type']
    except:  # # return an error if something goes wrong
        return Response({"message": "request has no type"}, status=status.HTTP_400_BAD_REQUEST)

    if item_type.lower() == 'post':
      # # get the Post serializer
      # post_serializer = PostSerializer(data=request.data)

      # # update the Inbox data if the serializer is valid
      # if post_serializer.is_valid():
      if postIsInInbox(request.data, inbox):
        return Response({"message": "Inbox item already exists"}, 
        status=status.HTTP_409_CONFLICT)
      
      inbox.items.append(request.data)
      inbox.save()
      return Response({"message": "Inbox item added", "data": serializer.data}, 
        status=status.HTTP_201_CREATED)

    elif item_type.lower() == 'follow':
      try:  # try to get the author and potential follower
        print("\n\Follow Object\n" + str(request.data) + "\n\n")
        follow_actor = request.data['actor']
        follow_object = request.data['object']
        if str(follow_object['id'])[:50] != str(authorObject.id)[:50]:
          raise ValueError("Follow object is not the same as Inbox Author")
        # actor_serializer = AuthorSerializer(data=follow_actor)
        # object_serializer = AuthorSerializer(data=follow_object)
        # if actor_serializer.is_valid() and object_serializer.is_valid():
        #   # Author.objects.get(id=follow_actor['id'])
        #   # Author.objects.get(id=follow_object['id'])
        #   pass
      except:  # return an error if something goes wrong
        return Response({"message": "Follow object is not the same as Inbox Author", "data": request.data}, status=status.HTTP_404_NOT_FOUND)

      #  "data": serializer.data raises an error
      if follow_actor['id'] == follow_object['id']:
          return Response({"message": "Self-following is prohibited."}, 
            status=status.HTTP_409_CONFLICT)
      try:
        Author.objects.get(id=follow_object['id']).followers.get(id=follow_actor['id'])
        return Response({"message": "Already following."}, 
          status=status.HTTP_409_CONFLICT)
      except:
        if followIsInInbox(request.data, inbox):
          return Response({"message": "Inbox item already exists"}, 
          status=status.HTTP_409_CONFLICT)
        
        inbox.items.append(request.data)
        inbox.save()
        return Response({"message": "Inbox item added"}, 
          status=status.HTTP_201_CREATED)

    elif item_type.lower() == 'like':
      try:
        print("\n\nLike Object\n" + str(request.data) + "\n\n")
        # # get the Like serializer
        # like_serializer = LikeSerializer(data=request.data)

        # # update the Inbox data if the serializer is valid
        # if like_serializer.is_valid():
        if likeIsInInbox(request.data, inbox):
          return Response({"message": "Inbox item already exists"}, 
          status=status.HTTP_409_CONFLICT)
        
        inbox.items.append(request.data)
        print("pre-save\n\n")
        inbox.save()
        return Response({"message": "Inbox item added", "data": request.data}, 
          status=status.HTTP_201_CREATED)
        # else:
        #   return Response({"message": "Like object is invalid"}, 
        #   status=status.HTTP_400_BAD_REQUEST)
      except:
        return Response({"message": "Like object cannot be serialized!"}, 
          status=status.HTTP_400_BAD_REQUEST)

    else:
      # return an error if something goes wrong with the update
      return Response({"message": "Item type must be `post`, `follow` or `like`!"}, 
        status=status.HTTP_400_BAD_REQUEST)

  # List all the things in the author's inbox
  if request.method == 'GET':
    try:  # try to get the inbox items
        author = Author.objects.get(uuid=author_uuid)
        inbox = Inbox.objects.get(author=author.id)
    except:  # return an error if something goes wrong
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # # if the logged in user is not the author
    # if not loggedInUserIsAuthor(request, author_uuid):  
    #   return Response(status=status.HTTP_401_UNAUTHORIZED)
    # else:  # if the logged in user is the author
    loggedInAuthorObject = getLoggedInAuthorObject(request)
    # if the logged in user does not have an Author object
    if loggedInAuthorObject is None:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # get the page number and size
    page_number = getPageNumber(request)
    page_size = getPageSize(request)

    # get the paginated inbox
    paginated_inbox = getPaginatedObject(inbox.items, page_number, page_size)

    # create the `type` field for the Posts data
    new_data = {'type': "inbox", 'author': author.id}

    # add the `type` field to the Posts data
    new_data.update({
        'items': paginated_inbox.object_list,
    })

    # return the Inbox data
    return Response(new_data, status=status.HTTP_200_OK)
  
  # Delete the inbox
  elif request.method == 'DELETE':
    try:  # try to get the inbox
      inbox = Inbox.objects.get(author=authorObject.id)
    except:  # return an error if something goes wrong
      return Response(status=status.HTTP_404_NOT_FOUND)
    
    # if the logged in user is not the author
    if not loggedInUserIsAuthor(request, author_uuid):  
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:  # if the logged in user is the author
      loggedInAuthorObject = getLoggedInAuthorObject(request)
      # if the logged in user does not have an Author object
      if loggedInAuthorObject is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # clear the inbox
    inbox.items.clear()
    inbox.save()

    # return a deletion message
    return Response({"message": "Inbox cleared"}, 
      status=status.HTTP_204_NO_CONTENT)
  
  # Handle unaccepted methods
  else:
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
