        program test77gtd7
        implicit none


        real D(9), T(2)

        call GTD7(172,29000.,400.,60.,-70.,16.,150.,150.,4.,48,D,T)


        write (*,*) D,T
        stop
        end
