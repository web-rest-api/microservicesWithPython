user-service------------	users
game-service-----------	games
activity-service-----------	activities
notification-service-------------	notifications

__________________________________________________________________________________________

How do services talk to each other?-----------------

activity-service → notification-service
Trigger: user logs activity
Protocol: RabbitMQ async event
Payload:
{
  activity_id,
  user_id,
  game_id,
  action
}

__________________________________________________________________________________________

# GameHub Service Map


                  [ Frontend ]
                        |
                    [ Gateway ]
       _________________|__________________
      |                 |                  |
[user-service]   [game-service]   [activity-service]
                                              |
                     --------------------------
                     |                        |
               (RabbitMQ)                (Kafka)
                     |                        |
       [notification-service]     [logging-service]

                        |
                 [auth-service]



________________________________________________________________________________________


